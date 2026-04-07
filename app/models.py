from pydantic import BaseModel, Field
from typing import Dict, Optional

class ResourceState(BaseModel):
    boats: int = 0
    ambulances: int = 0
    food_kits: int = 50

class State(BaseModel):
    # Location Header
    region: str = "Zone A"
    lat: float = 26.2
    lon: float = 91.7
    
    # Weather & Hazards
    disaster: str = "flood"
    severity: float = 0.5  # 0.0 to 1.0
    rainfall: float = 0.0
    forecast: str = "Calculating..."
    altitude: float = 100.0
    terrain: str = "lowland"
    
    # Infrastructure & Access
    road_blocked: bool = False
    traffic: str = "Low"
    rescue_access: str = "Good"
    resources: ResourceState = Field(default_factory=ResourceState)
    
    # Impact Panel (Winning Feature)
    population: int = 1000
    casualties: int = 0
    time_sensitivity: str = "CRITICAL"
    
    # Meta
    step: int = 1
    timestamp: float = 0.0
    last_action: Optional[Dict] = None

class Action(BaseModel):
    decision: str = Field(..., description="'evacuate', 'wait', or 'deploy_resources'")
    method: str = Field("standard", description="e.g. 'boats', 'helicopter', 'road'")
    priority: str = Field("medium", description="'low', 'medium', 'high'")
    resource_use: Dict[str, int] = Field(default_factory=dict, description="e.g. {'boats': 1}")
    target_region: str
    reasoning: str
    risk: Optional[str] = "Low"
