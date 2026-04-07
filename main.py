import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import google.generativeai as genai
from app.env import DisasterEnv
from app.models import Action

app = FastAPI(title="Disaster Response OpenEnv - Infrastructure Logic Engine")
env = DisasterEnv()

# Serve Frontend
if os.path.exists("frontend"):
    # Mount frontend directory for assets
    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", "r") as f:
        return f.read()

@app.get("/script.js")
def get_script():
    with open("frontend/script.js", "r") as f:
        return f.read()

@app.get("/api/status")
def status():
    return {
        "status": "active", 
        "env": "Disaster Response OpenEnv", 
        "regions": ["Zone A", "Zone B", "Zone C", "Zone D"],
        "compliance": "OpenEnv v1.2"
    }

@app.get("/reset")
def reset(scenario_id: int = None):
    """
    Resets the disaster environment.
    """
    state_obj = env.reset(scenario_id=scenario_id)
    return state_obj.model_dump()

@app.post("/step")
def step(action: Action):
    """
    Steps the environment with the agent's action.
    """
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": round(reward, 3),
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    """
    Returns the internal ground truth state.
    """
    return env.state()

@app.get("/run-agent")
async def run_agent():
    """
    Triggers the Gemini Agent to analyze the current state and take an action.
    """
    current_state = env.state()
    
    # Configure Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "API Key not configured"}
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
    You are a Disaster Response AI Agent.
    Current Situation:
    Region: {current_state['region']} ({current_state['lat']}, {current_state['lon']})
    Disaster: {current_state['disaster']}
    Severity: {current_state['severity']*100}%
    Weather: Rainfall={current_state['rainfall']}mm, Forecast={current_state['forecast']}
    Terrain: {current_state['terrain']}
    Infrastructure: Road Blocked={current_state['road_blocked']}, Traffic={current_state['traffic']}, Access={current_state['rescue_access']}
    Resources: {current_state['resources']}
    Impact: Population={current_state['population']}, Casualties={current_state['casualties']}, Sensitivity={current_state['time_sensitivity']}

    Task: Decide on the best action. 
    Output EXACTLY a JSON object:
    {{
        "decision": "evacuate" | "wait" | "deploy_resources",
        "method": "boats" | "helicopter" | "road" | "standard",
        "priority": "low" | "medium" | "high",
        "resource_use": {{"boats": 0, "ambulances": 0, "food_kits": 0}},
        "target_region": "{current_state['region']}",
        "reasoning": "Short explanation referencing sensors",
        "risk": "Low" | "Medium" | "High"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text.strip().replace("```json", "").replace("```", "")
        action_data = json.loads(content)
        
        # Step the environment
        action_obj = Action(**action_data)
        obs, reward, done, info = env.step(action_obj)
        
        return {
            "success": True,
            "action": action_data,
            "info": info
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Make sure we're in the right directory when running
    uvicorn.run(app, host="0.0.0.0", port=7860)
