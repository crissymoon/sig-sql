import math
from typing import List, Dict, Any

def sigmoid(x: float) -> float:
    try:
        clamped_x = max(-500, min(500, x))
        return 1 / (1 + math.exp(-clamped_x))
    except (OverflowError, ValueError, ZeroDivisionError):
        return 0.0 if x < 0 else 1.0

def multi_layer_sigmoid(x: float, layers: List[Dict[str, float]]) -> float:
    current_value = x
    for layer in layers:
        weight = layer.get('weight', 1.0)
        bias = layer.get('bias', 0.0)
        current_value = sigmoid(current_value * weight + bias)
    return current_value
