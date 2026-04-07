import time
import random
from typing import Tuple, Dict, Any
from .models import State, Action, ResourceState
from .data import get_random_scenario, get_scenario_by_id, REGIONS
from .grader import grade
from .reward import calculate_reward

class DisasterEnv:
    def __init__(self):
        self._state = State()
        self.reset()

    def reset(self, scenario_id: int = None) -> State:
        if scenario_id:
            data = get_scenario_by_id(scenario_id)
        else:
            data = get_random_scenario()
            
        region_data = REGIONS[data["region_idx"]]
        
        self._state = State(
            region=region_data["name"],
            lat=region_data["lat"],
            lon=region_data["lon"],
            
            disaster=data.get("disaster", region_data["risk"]),
            severity=data["severity"],
            rainfall=data["rainfall"],
            forecast=data["forecast"],
            altitude=region_data["altitude"],
            terrain=region_data["terrain"],
            
            road_blocked=data["road_blocked"],
            traffic=data.get("traffic", "Low"),
            rescue_access=data.get("rescue_access", "Good"),
            resources=ResourceState(**data["resources"]),
            
            population=region_data["population"],
            casualties=0,
            time_sensitivity="CRITICAL" if data["severity"] > 0.7 else "MODERATE",
            
            step=1,
            timestamp=time.time(),
            last_action=None
        )
        return self._state

    def step(self, action: Action) -> Tuple[State, float, bool, Dict[str, Any]]:
        # Calculate scores
        res = grade(action.model_dump(), self._state.model_dump())
        score = res["score"]
        feedback = res["feedback"]
        
        # Consequence Modeling (Logic Core)
        is_high_risk = self._state.severity > 0.7
        is_waiting = action.decision == "wait"
        
        if is_high_risk and is_waiting:
            # Casualty spike on waiting in critical situation
            new_casualties = random.randint(15, 45)
            self._state.casualties += new_casualties
            # Severity increases if ignored
            self._state.severity = min(1.0, self._state.severity + 0.05)
            feedback.append(f"CRITICAL DELAY: {new_casualties} reported casualties due to inactivity.")
        elif is_high_risk and action.decision == "evacuate":
            feedback.append("Timely evacuation saved lives.")
            # Severity might stabilize
            self._state.severity = max(0.0, self._state.severity - 0.1)
        elif action.decision == "deploy_resources":
            feedback.append(f"Resources deployed: {action.method}")
            self._state.severity = max(0.0, self._state.severity - 0.05)
            
        reward = calculate_reward(score, self._state.step)
        
        # Update last action for UI
        self._state.last_action = {
            **action.model_dump(),
            "feedback": feedback,
            "score": score
        }
        
        # Logic to "resolve" or progress
        done = True if self._state.step >= 5 or self._state.severity <= 0.1 else False
        self._state.step += 1
        self._state.timestamp = time.time()
        
        info = {
            "score": score,
            "feedback": feedback,
            "message": "Situation Updated."
        }
        
        return self._state, reward, done, info

    def state(self) -> Dict[str, Any]:
        data = self._state.model_dump()
        # Add a "last updated" string for the UI feel
        data["last_updated_str"] = time.strftime("%H:%M:%S", time.localtime(data["timestamp"]))
        return data
