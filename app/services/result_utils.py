# app/services/result_utils.py

def color_sequence(sequence):
    color_map = {
        'H': '#FFC107',  # Yellow for Helix
        'E': '#FFFFFF',  # White for Sheet
        'C': '#87CEEB',  # Light blue for Coil
    }
    colored_sequence = []
    for char in sequence:
        color = color_map.get(char, '#FFFFFF')
        colored_sequence.append((char, color))
    return colored_sequence

def generate_insights(sequence):
    from collections import Counter
    counts = Counter(sequence)
    total = len(sequence)
    if total == 0:
        return ["No sequence data available."]

    insights = []

    if counts.get('H', 0) / total > 0.4:
        insights.append("High proportion of helices suggests structural stability.")
    if counts.get('E', 0) / total > 0.3:
        insights.append("Significant amount of sheets indicates possible stable interactions.")
    if counts.get('C', 0) / total > 0.3:
        insights.append("Coil regions indicate flexibility in the protein structure.")

    if not insights:
        insights.append("Balanced distribution suggests a versatile protein structure.")

    return insights
