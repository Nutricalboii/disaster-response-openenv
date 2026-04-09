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

TriNetra is a high-fidelity OpenEnv environment designed to evaluate how AI agents make decisions in disaster response scenarios involving uncertainty, limited resources, and conflicting signals.

It focuses on structured, multi-step decision-making where each action has measurable consequences under operational constraints.

---

## Problem Context

Disaster response involves complex, high-pressure decision-making:

- Signals from telemetry and reports may be inconsistent or misleading  
- Infrastructure conditions evolve rapidly  
- Resources are constrained and must be allocated carefully  
- Decisions must be made under strict time and budget limits  

Traditional evaluation setups do not capture these conditions effectively.

---

## Approach

TriNetra models crisis operations as a sequence of decisions where an agent must:

- interpret situational reports (SITREP)  
- distinguish signal from noise  
- allocate resources under budget constraints  
- maintain consistency across evolving states  

The environment emphasizes process-level evaluation rather than isolated outputs.

---

## Observation Space

Each step provides a structured state:

- `task_id` — active task  
- `intelligence_report` — situational summary  
- `telemetry_data` — sensor readings (weather, terrain, drainage)  
- `available_resources` — counts of deployable assets  
- `logistics_budget` — financial constraint (starting at 100,000)  

---

## Action Space

The agent must return a structured response:

- `threat_level` — low / medium / high  
- `deploy_region` — selected region  
- `budget_scratchpad` — cost calculation within constraints  
- `resource_allocation` — deployment plan  
- `reasoning` — justification  

---

## Tasks

### triage_basic (Easy)
- Identify threat correctly  
- Choose appropriate response  

### resource_allocation (Medium)
- Match resources to scenario  
- Stay within budget  

### signal_vs_noise (Hard)
- Filter misleading alerts  
- Act on subtle but critical signals  

---

## Evaluation

Scores range from **0.0 to 1.0** based on:

- correctness of classification  
- resource allocation accuracy  
- adherence to constraints  
- consistency across steps  

### Constraints

- incorrect region selection reduces score  
- incorrect resource usage reduces score  
- exceeding budget results in score = 0.0  

---

## System Architecture

TriNetra uses a multi-agent structure:

- **Agent Alpha (Intelligence):** processes signals and extracts relevant information  
- **Agent Beta (Logistics):** computes cost-aware deployment decisions  

### Procedural Generation

Scenarios are generated dynamically using:

- varying weather conditions  
- terrain differences  
- sensor inconsistencies  

This prevents memorization and ensures robustness.

---

## Baseline Evaluation

Model: Qwen/Qwen2.5-72B-Instruct  
Execution: Hugging Face Inference API  

| Task | Score |
|------|------|
| triage_basic | 1.00 |
| resource_allocation | 1.00 |
| signal_vs_noise | 1.00 |

Results are deterministic and reproducible.

---

## Setup

### Clone
git clone https://github.com/username/trinetra.git
cd trinetra


### Install
pip install uv
uv sync


### Environment Variables

Create `.env`:
HF_TOKEN=your_token
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
API_BASE_URL=https://router.huggingface.co/v1


---

## Run
python -m server.app


Open:
http://localhost:7860


---

## Inference
python inference.py


---

## Docker
docker build -t trinetra-engine .
docker run -p 7860:7860 --env-file .env trinetra-engine


---

## Repository Structure
app/ environment + grading logic
frontend/ dashboard interface
server/ backend service
inference.py evaluation script
openenv.yaml environment config
Dockerfile container setup


---

## Design Focus

TriNetra evaluates:

- decision-making under uncertainty  
- ability to filter conflicting signals  
- resource prioritization under constraints  
- consistency across sequential steps  

---

## Notes

- scoring is deterministic  
- evaluation is reproducible  
- financial constraints are strictly enforced  

---

## Team

## Team

- Vaibhav Sharma ([Nutricalboii](https://github.com/Nutricalboii))  
- Anushka Rawat ([Anushka130126](https://github.com/Anushka130126))  
- Devesh Khurana ([DeveshKhurana1-oss](https://github.com/DeveshKhurana1-oss))  
