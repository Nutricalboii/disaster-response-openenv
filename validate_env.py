import sys
import requests
import json
import time

URL = "http://localhost:7860"

def run_checks():
    print("--- Disaster Response OpenEnv Validation ---")
    
    try:
        # Check reset
        print("[CHECK] resetting environment...")
        obs = requests.get(f"{URL}/reset").json()
        print(f"Observation: {json.dumps(obs, indent=2)}")
        
        # Check step
        print("\n[CHECK] taking evacuation step...")
        action = {
            "decision": "evacuate",
            "resource_use": {"boats": 1} if obs["road_blocked"] else {},
            "target_region": obs["region"],
            "reasoning": "Standard evacuation protocol based on rainfall.",
            "risk": "High" if obs["severity"] > 0.7 else "Low"
        }
        res = requests.post(f"{URL}/step", json=action).json()
        print(f"Result: {json.dumps(res, indent=2)}")
        
        # Check score
        score = res["info"]["score"]
        print(f"\n[PASSED] Step score: {score}")
        
        if score > 0:
            print("[SUCCESS] Logic is functional.")
        else:
            print("[WARNING] Zero score - check grader logic or scenario mismatch.")
            
    except Exception as e:
        print(f"[FAILED] Error during validation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_checks()
