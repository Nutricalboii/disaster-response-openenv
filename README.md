<h1 align="center">TriNetra: Autonomous Crisis Operations Engine</h1>

<p align="center">
  <img src="https://img.shields.io/badge/OpenEnv-Compliant-green" />
  <img src="https://img.shields.io/badge/Docker-Ready-blue" />
  <img src="https://img.shields.io/badge/Deploy-HuggingFace-orange" />
  <img src="https://img.shields.io/badge/Scoring-Deterministic-critical" />
  <img src="https://img.shields.io/badge/Architecture-Multi--Agent-purple" />
</p>

<p align="center">
  A structured environment for evaluating AI decision-making in high-stakes disaster scenarios
</p>

---

## Overview

TriNetra is a high-fidelity, multi-agent simulation environment built on the OpenEnv framework. It serves as a structured evaluation system for AI agents operating in disaster response scenarios involving uncertainty, limited resources, and conflicting signals.

---

## Environment Motivation

Disaster response coordinators operate under severe cognitive load:

- Multiple data sources (IoT telemetry, weather signals, reports) may conflict  
- Infrastructure conditions change rapidly  
- Resource pools are limited  
- Decisions must be made under strict financial constraints  

TriNetra models this decision process by simulating the role of an Emergency Operations Director — identifying real threats ("signal") from misleading inputs ("noise") and deploying resources within a fixed operational budget.

---

## Observation Space

The environment emits a structured Pydantic JSON state:

- `task_id` — current task  
- `intelligence_report` — situational summary (SITREP)  
- `telemetry_data` — raw sensor data (weather, terrain, drainage)  
- `available_resources` — boats, ambulances, food kits  
- `logistics_budget` — financial constraint (starting at 100,000)  

---

## Action Space

The agent must respond with a structured Pydantic JSON:

- `threat_level` — low / medium / high  
- `deploy_region` — region extracted from SITREP  
- `budget_scratchpad` — cost calculation (Boats: 5k, Ambulances: 2k, Food: 50)  
- `resource_allocation` — deployment plan  
- `reasoning` — justification  

---

## Tasks

TriNetra includes three procedurally generated tasks with deterministic grading:

### triage_basic (Easy)
- Classify threat using terrain and weather  
- Prioritize correct response  

### resource_allocation (Medium)
- Match resources to scenario  
- Stay within budget constraints  

### signal_vs_noise (Hard)
- Filter misleading alerts  
- Identify real crisis signals  
- Deploy resources correctly  

---

## Evaluation

Scores range from **0.0 to 1.0**, based on:

- threat classification accuracy  
- resource allocation correctness  
- budget adherence  
- signal vs noise handling  

### Constraints

- incorrect region → penalty  
- incorrect resource → penalty  
- exceeding budget → score = 0.0  

---

## Baseline Performance

Baseline evaluation uses a multi-agent swarm architecture:

- **Agent Alpha (Intelligence):** filters signals  
- **Agent Beta (Logistics):** performs cost reasoning  

Model: `Qwen/Qwen2.5-72B-Instruct`

| Task | Difficulty | Score |
|------|-----------|------|
| triage_basic | Easy | 1.00 |
| resource_allocation | Medium | 1.00 |
| signal_vs_noise | Hard | 1.00 |

Scores are deterministic and reproducible.

---

## System Architecture

TriNetra uses a Multi-Agent Swarm design to reduce reasoning errors and improve decision clarity:

- Separation of intelligence and logistics  
- Structured decision pipeline  
- Reduced hallucination risk  

### Procedural Generation

- Dynamic scenarios (weather, terrain, failures)  
- Prevents memorization  
- Ensures robustness across runs  

---

## Setup

### Clone Repository
git clone https://github.com/username/trinetra.git
cd trinetra


---

### Install Dependencies
pip install uv
uv sync


---

### Configure Environment

Create `.env`:
HF_TOKEN=your_huggingface_token
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
API_BASE_URL=https://router.huggingface.co/v1


---

## Run Environment
python -m server.app


Open:
http://localhost:7860


---

## Run Inference
python inference.py


---

## Docker Deployment
docker build -t trinetra-engine .
docker run -p 7860:7860 --env-file .env trinetra-engine


---

## Repository Structure
app/ environment + grader
frontend/ UI dashboard
server/ backend
inference.py evaluation script
openenv.yaml environment spec
Dockerfile container setup


---

## Design Focus

This environment evaluates:

- decision-making under uncertainty  
- filtering conflicting signals  
- resource prioritization under constraints  
- consistency across sequential steps  

---

## Notes

- scoring is deterministic  
- evaluation is reproducible  
- budget constraints are strictly enforced  

---

## Team

<p align="center">
  <b>Vaibhav Sharma</b><br>
  <a href="https://github.com/Nutricalboii">Nutricalboii</a>
  <br><br>

  <b>Anushka Rawat</b><br>
  <a href="https://github.com/Anushka130126">Anushka130126</a>
  <br><br>

  <b>Devesh Khurana</b><br>
  <a href="https://github.com/DeveshKhurana1-oss">DeveshKhurana1-oss</a>
</p>
