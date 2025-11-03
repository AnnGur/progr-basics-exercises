def get_letter_grade(score):
    """
    Convert score to letter grade.
    A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: below 60
    """
    if not isinstance(score, (int, float)):
        return "Invalid score"
    if score < 0 or score > 100:
        return "Invalid score"
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"