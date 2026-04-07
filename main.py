import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
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
    return state_obj.dict()

@app.post("/step")
def step(action: Action):
    """
    Steps the environment with the agent's action.
    """
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
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

if __name__ == "__main__":
    import uvicorn
    # Make sure we're in the right directory when running
    uvicorn.run(app, host="0.0.0.0", port=7860)
