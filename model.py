import random

def predict_probabilities(match):
    return {
        "home": random.uniform(0.35, 0.55),
        "draw": random.uniform(0.20, 0.30),
        "away": random.uniform(0.30, 0.50)
    }