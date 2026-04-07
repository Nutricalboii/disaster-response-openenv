# Architecture of Disaster Response OpenEnv

## 1. System Overview
The Disaster Response OpenEnv is a modular, high-fidelity environment designed for disaster scenario simulation. It adheres to the **OpenEnv v1.2 Standard**, ensuring interoperability with various AI agent architectures.

## 2. Component Layers

### A. Environment Core (`app/env.py`)
- **State Management**: Using Pydantic models for type-safe state tracking.
- **Scenario Injection**: Dynamic loading of diverse disaster profiles (flood, fire, highland/lowland).

### B. Logic & Grading (`app/grader.py`, `app/reward.py`)
- **Deterministic Grading**: Scoring is based on rule-based logic to evaluate decision correctness.
- **Efficiency Rewarding**: Penalizes step latency to encourage faster crisis response.

### C. Resource Profiling (`app/data.py`)
- **Scenario Traps**: Models "Fake Urgency" (low risk, high noise) and "Silent Crisis" (high risk, low visibility) to test agent robustness.

### D. Interface Layers
- **UI System (`frontend/`)**: High-accessibility, multi-language dashboard (HTML/JS/CSS).
- **Agent API (`main.py`)**: FastAPI-powered REST interface for `/reset`, `/step`, and `/state`.
- **Inference Pipeline (`inference.py`)**: Standardized agent interaction baseline.

## 3. Data Flow
1. **Reset**: Environment selects a scenario from `data.py`.
2. **Observation**: State is exposed via `State` model.
3. **Action**: Agent submits an `Action` model.
4. **Grading**: `grader.py` evaluates the `Action` against the `State`.
5. **Reward**: `reward.py` computes total reward with step penalties.
6. **UI Update**: Frontend polls `/state` to reflect the latest situational awareness.

## 4. Evaluation Metrics
- **Success Rate**: Correct identifies required evacuations.
- **Resource Efficiency**: Optimal usage of boats vs. ambulances.
- **Reasoning Quality**: Alignment of internal reasoning with ground truth telemetry.
