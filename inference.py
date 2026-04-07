import os
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables (API Key)
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

if not os.environ["GOOGLE_API_KEY"]:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")
TASK_NAME = "disaster_response_evacuation"

def run_inference():
    print(f"[START] task={TASK_NAME} env=disaster-response-openenv model=gemini-1.5-flash")
    
    try:
        obs = requests.get(f"{ENV_URL}/reset").json()
    except Exception as e:
        print(f"[END] success=false steps=0 score=0.0 rewards=[] error={str(e)}")
        return

    done = False
    step = 0
    total_score = 0.0
    rewards = []

    while not done and step < 5:
        # Construct Prompt for Gemini
        prompt = f"""
        You are a Disaster Response AI Agent.
        Current Situation:
        Region: {obs['region']} ({obs['lat']}, {obs['lon']})
        Disaster: {obs['disaster']}
        Severity: {obs['severity']*100}%
        Weather: Rainfall={obs['rainfall']}mm, Forecast={obs['forecast']}
        Terrain: {obs['terrain']}
        Infrastructure: Road Blocked={obs['road_blocked']}, Traffic={obs['traffic']}, Access={obs['rescue_access']}
        Resources: {obs['resources']}
        Impact: Population={obs['population']}, Casualties={obs['casualties']}, Sensitivity={obs['time_sensitivity']}

        Task: Decide on the best action. 
        Output EXACTLY a JSON object:
        {{
            "decision": "evacuate" | "wait" | "deploy_resources",
            "method": "boats" | "helicopter" | "road" | "standard",
            "priority": "low" | "medium" | "high",
            "resource_use": {{"boats": 0, "ambulances": 0, "food_kits": 0}},
            "target_region": "{obs['region']}",
            "reasoning": "Short explanation referencing sensors",
            "risk": "Low" | "Medium" | "High"
        }}
        """

        try:
            response = model.generate_content(prompt)
            # Remove markdown code blocks if present
            content = response.text.strip().replace("```json", "").replace("```", "")
            action = json.loads(content)
            
            res = requests.post(f"{ENV_URL}/step", json=action).json()
            
            reward = res["reward"]
            done = res["done"]
            info = res["info"]
            obs = res["observation"]
            
            total_score += info.get("score", 0.0)
            rewards.append(reward)
            
            print(f"[STEP] step={step} action={json.dumps(action)} reward={reward:.2f} done={str(done).lower()} error=null")
            step += 1
            
        except Exception as e:
            print(f"[STEP] step={step} action=null reward=0.00 done=true error={str(e)}")
            done = True

    final_score = round(total_score / max(1, step), 2)
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success=true steps={step} score={final_score} rewards={rewards_str}")

if __name__ == "__main__":
    run_inference()
