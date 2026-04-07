from typing import Dict, Any

def grade(action: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    score = 0.0
    feedback = []

    # 1. Decision Logic (0.4)
    is_severe = state["severity"] > 0.65
    is_evacuating = action["decision"] == "evacuate"
    
    if is_severe and is_evacuating:
        score += 0.4
        feedback.append("Correct evacuation decision.")
    elif not is_severe and action["decision"] == "wait":
        score += 0.4
        feedback.append("Correct wait decision - no high alert.")
    else:
        feedback.append("Incorrect primary decision for this risk level.")

    # 2. Resource/Method Match (0.2)
    # If roads blocked and boats used
    if state["road_blocked"]:
        if "boat" in action.get("method", "").lower() or action["resource_use"].get("boats", 0) > 0:
            score += 0.2
            feedback.append("Correct method used for blocked infrastructure.")
        else:
            feedback.append("Method suboptimal: Road access blocked, but boats not prioritized.")
    else:
        score += 0.2
        feedback.append("Method appropriate for terrain.")

    # 3. Reasoning Context (0.2)
    # Check for keywords related to the risk (e.g. rain, river, mountain)
    keywords = ["rain", "river", "flood", "mountain", "upstream", "water", "altitude", "population"]
    found_keywords = [k for k in keywords if k in action.get("reasoning", "").lower()]
    if len(found_keywords) >= 2:
        score += 0.2
        feedback.append(f"Strong reasoning referencing context: {', '.join(found_keywords)}")
    elif len(found_keywords) == 1:
        score += 0.1
        feedback.append("Partial reasoning context detected.")

    # 4. Noise & Overreaction (0.2)
    # Trap check: Fake Alert
    if "URGENT" in state.get("description", "") and state["severity"] < 0.3:
        if action["decision"] == "wait":
            score += 0.1 # Ignored noise
            feedback.append("Excellent: Ignored fake alert noise.")
        else:
            feedback.append("Failed trap: Over-reacted to fake urgency message.")
    else:
        score += 0.1 # Standard logic

    if state["severity"] < 0.5 and action["priority"] == "low":
        score += 0.1 # Avoided overreaction
        feedback.append("Appropriate priority level.")
    elif state["severity"] > 0.8 and action["priority"] == "high":
        score += 0.1 # Responsive to high risk
        feedback.append("Good situational urgency.")

    final_score = round(max(0.0, min(1.0, score)), 2)
    return {
        "score": final_score,
        "feedback": feedback
    }
