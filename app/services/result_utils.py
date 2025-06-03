# app/services/result_utils.py

from fpdf import FPDF
import os
from transformers import pipeline, AutoTokenizer, TFAutoModelForCausalLM

# Load once at startup
insight_generator = pipeline(
    "text-generation",
    model=TFAutoModelForCausalLM.from_pretrained("gpt2"),
    tokenizer=AutoTokenizer.from_pretrained("gpt2")
)

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
    structure_path = os.path.join("app", "assets", f"structure_{prediction_uuid}.png")
    if os.path.exists(structure_path):
        pdf.image(structure_path, w=150)
        pdf.ln(10)

    # Pie Chart
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Predicted Protein Structure Distribution", ln=True)
    pie_chart_path = os.path.join("app", "assets", f"pie_chart_{prediction_uuid}.png")
    if os.path.exists(pie_chart_path):
        pdf.image(pie_chart_path, w=100)
        pdf.ln(10)

    # Bar Chart
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Comparison with Known Protein Data", ln=True)
    bar_chart_path = os.path.join("app", "assets", f"bar_chart_{prediction_uuid}.png")
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
    prompt = (
        "Analyze the following protein secondary structure sequence "
        "in HEC format and generate biological insights and functional implications:\n"
        f"{sequence}\n\nInsights:"
    )
    result = insight_generator(prompt, max_length=250, temperature=0.7, num_return_sequences=1)
    insight_text = result[0]['generated_text'][len(prompt):].strip()  # Remove prompt from output
    return insight_text
