# app/services/result_utils.py

from fpdf import FPDF
import os

def generate_pdf(sequence, insights, prediction_uuid, output_path=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Protein Sequence Prediction Result", ln=True, align="C")
    pdf.ln(10)

    # Sequence
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Sequence:", ln=True)
    pdf.set_font("Arial", "", 12)
    sequence_lines = [sequence[i:i+80] for i in range(0, len(sequence), 80)]
    for line in sequence_lines:
        pdf.cell(0, 8, line, ln=True)
    pdf.ln(10)

    # Insights
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Insights:", ln=True)
    pdf.set_font("Arial", "", 12)
    for insight in insights:
        pdf.multi_cell(0, 8, f"- {insight}")
    pdf.ln(10)

    # Structure Image
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Structure Image", ln=True)
    structure_path = os.path.join("app", "assets", f"{prediction_uuid}", f"structure.png")
    if os.path.exists(structure_path):
        pdf.image(structure_path, w=150)
        pdf.ln(10)

    # Pie Chart
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Predicted Protein Structure Distribution", ln=True)
    pie_chart_path = os.path.join("app", "assets", f"{prediction_uuid}", f"pie_chart.png")
    if os.path.exists(pie_chart_path):
        pdf.image(pie_chart_path, w=100)
        pdf.ln(10)

    # Bar Chart
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Comparison with Known Protein Data", ln=True)
    bar_chart_path = os.path.join("app", "assets", f"{prediction_uuid}", f"bar_chart.png")
    if os.path.exists(bar_chart_path):
        pdf.image(bar_chart_path, w=120)

    # Save to file
    if not output_path:
        output_path = f"Protein_Prediction_Result_{prediction_uuid}.pdf"
    pdf.output(output_path)
    return output_path


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