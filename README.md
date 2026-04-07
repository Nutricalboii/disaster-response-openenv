# Disaster Response OpenEnv v2.0

A professional-grade disaster decision environment designed to evaluate AI agents on real-world crisis management logic.

## 🚀 Key Framework Features

### 1. Real-World Region Engine
Simulates realistic disaster zones with localized metadata:
- **Assam Flood Zone**: Brahamaputra river basin dynamics.
- **Himachal Landslide Zone**: Upstream dam release and high-altitude risk.
- **Mumbai Urban Flood**: High-population density drainage failure.
- **Odisha Cyclone Coast**: Storm surge and coastal vulnerability.

### 2. Decision Consequence Modeling
Unlike static environments, this system tracks the real-world impact of agent behavior:
- **Casualties Tracking**: Waiting in high-severity situations leads to simulated casualty spikes.
- **Time Sensitivity**: Situations are marked as **CRITICAL**, **MODERATE**, or **STABLE**, influencing grading.

### 3. Advanced Multi-Factor Grader
Scores agents on more than just "right or wrong":
- **Method Match**: rewards choosing boats when roads are blocked.
- **Reasoning Context**: Verifies if the agent mentions rainfall, altitude, or specific regional risks.
- **Noise Immunity**: Rewards agents that ignore "fake urgency" alerts but react to "silent crises".

### 4. Professional Command Dashboard
- **Location Awareness**: Lat/Lon coordinates and real-time region injection.
- **Weather Telemetry**: Rainfall and forecast monitoring.
- **Strategic Impact Panel**: Real-time tracking of population risk, casualties, and strategic score.
- **Bilingual & Accessible**: Native support for Hindi and English.

## 🛠️ Developer Setup

### Prerequisites
- Python 3.9+
- FastAPI, Uvicorn, Pydantic

### Quick Start
```bash
cd Disaster-Response-OpenEnv
# Use your virtual environment
python3 main.py
```
Visit `http://localhost:7860` for the dashboard.

## ⚖️ Evaluation Compliance
Standardized agent output format:
- `[START]`
- `[STEP]`
- `[END]`

Validates against **OpenEnv v1.2** standards for Disaster Resilience.

---
*Built for the Meta Hackathon - Disaster Response Track.*
