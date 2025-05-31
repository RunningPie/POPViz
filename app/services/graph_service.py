# app/services/graph_service.py
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import os
matplotlib.use("Agg")

# Define assets path properly
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'assets')

def generate_structure_dot_plot(sequence, filename="structure.png"):
    os.makedirs(ASSETS_FOLDER, exist_ok=True)
    save_path = os.path.join(ASSETS_FOLDER, filename)

    plt.figure(figsize=(len(sequence) // 5, 3))
    colors = {'H': 'gold', 'E': 'skyblue', 'C': 'lightgreen'}
    x = range(len(sequence))
    y = [0] * len(sequence)
    c = [colors.get(label, 'gray') for label in sequence]
    
    plt.scatter(x, y, c=c, s=100, edgecolors='black')
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def generate_pie_chart(sequence, filename="pie_chart.png"):
    from collections import Counter
    os.makedirs(ASSETS_FOLDER, exist_ok=True)
    save_path = os.path.join(ASSETS_FOLDER, filename)

    counts = Counter(sequence)
    labels = counts.keys()
    sizes = counts.values()
    colors = ['gold', 'skyblue', 'lightgreen']  # H, E, C

    plt.figure(figsize=(5,5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def generate_bar_chart(sequence, database_hec_avg, filename="bar_chart.png"):
    from collections import Counter
    os.makedirs(ASSETS_FOLDER, exist_ok=True)
    save_path = os.path.join(ASSETS_FOLDER, filename)

    counts = Counter(sequence)
    labels = ['H', 'E', 'C']
    sequence_avg = [counts.get(l, 0) / len(sequence) for l in labels]

    df = pd.DataFrame({
        "Structure": ["Helix", "Sheet", "Coil"],
        "Predicted": sequence_avg,
        "Database": database_hec_avg
    })

    plt.figure(figsize=(6, 4))
    bar_width = 0.35
    index = range(len(df))

    plt.bar(index, df['Predicted'], bar_width, label='Predicted', color='gold')
    plt.bar([i + bar_width for i in index], df['Database'], bar_width, label='Database', color='skyblue')

    plt.xlabel('Structure')
    plt.ylabel('Proportion')
    plt.xticks([i + bar_width/2 for i in index], df['Structure'])
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
