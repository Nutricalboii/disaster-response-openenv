import random
from typing import Dict, List, Any

# Strategic Layer: Region Engine
REGIONS = [
    {
        "name": "Assam Flood Zone",
        "lat": 26.2442,
        "lon": 91.7325,
        "terrain": "lowland",
        "risk": "river flood",
        "population": 2500,
        "altitude": 140
    },
    {
        "name": "Himachal Landslide Zone",
        "lat": 31.1048,
        "lon": 77.1734,
        "terrain": "hilly",
        "risk": "landslide",
        "population": 800,
        "altitude": 2205
    },
    {
        "name": "Mumbai Urban Flood",
        "lat": 19.0760,
        "lon": 72.8777,
        "terrain": "urban",
        "risk": "drainage failure",
        "population": 12000,
        "altitude": 14
    },
    {
        "name": "Odisha Cyclone Coast",
        "lat": 20.2724,
        "lon": 85.8338,
        "terrain": "coastal",
        "risk": "storm surge",
        "population": 5000,
        "altitude": 5
    }
]

SCENARIOS = [
    {
        "id": 1,
        "name": "Assam Severe River Flood",
        "region_idx": 0,
        "severity": 0.88,
        "rainfall": 160,
        "forecast": "HEAVY RAIN (Rising)",
        "road_blocked": True,
        "traffic": "HIGH",
        "rescue_access": "LIMITED",
        "resources": {"boats": 2, "ambulances": 1, "food_kits": 100},
        "description": "High water levels and blocked roads in the Brahmaputra basin."
    },
    {
        "id": 2,
        "name": "Fake Urgency Alert (Noise)",
        "region_idx": 1,
        "severity": 0.22,
        "rainfall": 10,
        "forecast": "SCATTERED SHOWERS",
        "road_blocked": False,
        "traffic": "LOW",
        "rescue_access": "GOOD",
        "resources": {"boats": 0, "ambulances": 2, "food_kits": 50},
        "description": "URGENT ALERT: Potential water level increase! But sensor data shows low risk."
    },
    {
        "id": 3,
        "name": "Silent Crisis (Detection)",
        "region_idx": 2,
        "severity": 0.75,
        "rainfall": 85,
        "forecast": "PERSISTENT DRIZZLE",
        "road_blocked": False,
        "traffic": "MODERATE",
        "rescue_access": "FAIR",
        "resources": {"boats": 4, "ambulances": 3, "food_kits": 500},
        "description": "Mumbai drainage systems failing. Low noise but criticial levels."
    },
    {
        "id": 5,
        "name": "Conflicting Signals (Trap)",
        "region_idx": 1,
        "severity": 0.65,
        "rainfall": 5,
        "forecast": "CLEAR SKIES",
        "road_blocked": False,
        "traffic": "LOW",
        "rescue_access": "GOOD",
        "resources": {"boats": 0, "ambulances": 1, "food_kits": 20},
        "description": "Clear skies but Himachal upstream dam release detected! Silent high-risk landslide/flood."
    },
    {
        "id": 6,
        "name": "Odisha Cyclonic Tidal Surge",
        "region_idx": 3,
        "severity": 0.95,
        "rainfall": 210,
        "forecast": "SEVERE CYCLONE",
        "road_blocked": True,
        "traffic": "NONE",
        "rescue_access": "LIMITED",
        "resources": {"boats": 10, "ambulances": 5, "food_kits": 1000},
        "description": "Massive storm surge in Odisha. Coastal roads submerged. Immediate rescue required."
    },
    {
        "id": 7,
        "name": "Mumbai Drainage Collapse",
        "region_idx": 2,
        "severity": 0.82,
        "rainfall": 120,
        "forecast": "EXTREME DOWNPOUR",
        "road_blocked": True,
        "traffic": "CHOKED",
        "rescue_access": "FAIR",
        "resources": {"boats": 5, "ambulances": 10, "food_kits": 200},
        "description": "Urban flooding in Mumbai. Drainage failure has led to waist-deep water in several sectors."
    },
    {
        "id": 8,
        "name": "Assam Flash Flood (Upstream)",
        "region_idx": 0,
        "severity": 0.78,
        "rainfall": 45,
        "forecast": "MILD SHOWERS",
        "road_blocked": False,
        "traffic": "MODERATE",
        "rescue_access": "FAIR",
        "resources": {"boats": 3, "ambulances": 2, "food_kits": 150},
        "description": "Rainfall is mild locally, but massive upstream discharge has created a sudden flash flood."
    }
]

def get_random_scenario() -> Dict[str, Any]:
    return random.choice(SCENARIOS)

def get_scenario_by_id(scenario_id: int) -> Dict[str, Any]:
    for s in SCENARIOS:
        if s["id"] == scenario_id:
            return s
    return SCENARIOS[0]
