def calculate_raw_score(severity: str) -> float:
    severity_scores = {
        "Low": 3.0,
        "Medium": 5.0,
        "High": 8.0,
        "Critical": 9.5
    }

    return severity_scores.get(severity, 0.0)