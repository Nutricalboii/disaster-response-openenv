# Disaster Response Demo Script

Use this script during your 2-minute Hackathon pitch to showcase the depth of the system.

## 🎤 The Pitch (2 Minutes)

### 00:00 - The Problem
"Most disaster response AI models either over-react to noise or under-react to silent crises. They see an 'URGENT' alert and evacuate immediately, or they wait too long when the sensor data is slightly above danger. This leads to wasted resources or, worse, casualties."

### 00:30 - The Solution
"We built **Disaster Response OpenEnv**. It's not just a dashboard; it's a decision-evaluation system that models real-world context like terrain, weather forecasts, and infrastructure access. We simulate **Assam’s river floods**, **Himachal’s landslides**, and **Mumbai’s urban drainage failures** with actual coordinates and population data."

### 01:00 - The Demo (Live Action)
"Let's look at the **Impact Panel**. Our system tracks **Current Casualties**. If an agent waits during a critical flood in Assam, our environment calculates a 'Consequence Spike'. Notice the **'Time Sensitivity'** indicator—it's currently CRITICAL."

### 01:30 - The Core Differentiation
"We implemented a **Multi-Factor Grader**. It doesn't just score 1 or 0. It evaluates **Method Match**—did the agent use boats when roads were blocked? It checks for **Noise Immunity**—did it ignore a fake 'URGENT' tag when the rain was only 5mm? It evaluates **Reasoning**—does the agent mention altitude or upstream dam releases?"

### 01:50 - The Conclusion
"Our platform ensures that the next generation of disaster response agents are not just fast, but **precise, robust, and life-saving**. Thank you."

---

## 🏗️ Demo Scenario Flow (Standard Evaluation)

**Scenario 1: The Fake Alert**
- **Action**: Reset to "Fake Urgency Alert (Noise)".
- **Observation**: UI shows 'URGENT' in description but Rainfall is only 10mm.
- **Agent Decision**: `wait`.
- **Outcome**: Strategic Score: **0.9+**. 
- **Commentary**: "The agent showed intelligence by ignoring the alarmist message and trusting the raw sensor data."

**Scenario 2: The Silent Crisis**
- **Action**: Reset to "Silent Crisis (Detection)".
- **Observation**: UI shows 'PERSISTENT DRIZZLE' but Severity is 75%.
- **Agent Decision**: `evacuate`.
- **Outcome**: Casualties: **0**.
- **Commentary**: "Even with low-noise weather, the agent identified the failing drainage infrastructure and acted before casualties occurred."

**Scenario 3: The Infrastructure Fail**
- **Action**: Reset to "Assam Severe River Flood".
- **Observation**: Roads are **BLOCKED**.
- **Agent Decision**: `evacuate` using `helicopter` or `boats`.
- **Outcome**: Method Match: **Bonus Points**.
- **Commentary**: "The agent identified that road evacuation was impossible and transitioned to watercraft specialized for the lowland terrain."
