def calculate_reward(score: float, step: int) -> float:
    # reward = score - min(0.15, step * 0.03)
    # Penalize longer steps to encourage efficient decisions
    penalty = min(0.15, step * 0.03)
    return round(score - penalty, 2)
