import os
import json
import requests
from typing import Dict, Any

# Environment configuration
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")
TASK_NAME = "disaster_response_evacuation"
MODEL_NAME = os.getenv("MODEL_NAME", "disaster-logic-v1")

def run_inference():
    """
    Disaster Response OpenEnv Baseline.
    Standardized agent interface for crisis management evaluation.
    """
    print(f"[START] task={TASK_NAME} env=disaster-response-openenv model={MODEL_NAME}")
    
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
        # Prompting logic (Simulated here or using an LLM)
        # For the baseline, we simulate a simple logic or wait for an LLM integration
        
        # In a real scenario, we'd pass 'obs' to an LLM. 
        # Here we define a structured decision based on the state.
        
        decision = "wait"
        resource_use = {}
        reasoning = "Analyzing data..."
        
        if obs["severity"] > 0.7:
            decision = "evacuate"
            reasoning = "High severity and rainfall detected. Immediate evacuation initiated."
            if obs["road_blocked"]:
                resource_use = {"boats": 1}
                reasoning += " Roads blocked, deploying watercraft."
        else:
            reasoning = "Conditions stable. Monitoring situation."

        action = {
            "decision": decision,
            "resource_use": resource_use,
            "target_region": obs["region"],
            "reasoning": reasoning,
            "risk": "Medium" if obs["severity"] > 0.5 else "Low"
        }

        try:
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
