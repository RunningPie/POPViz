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

    plt.figure(figsize=(len(sequence) // 2, 3))
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
    label_order = ['H', 'E', 'C']  # fixed order
    sizes = [counts.get(label, 0) for label in label_order]

    # Filter out labels with 0 size
    filtered_labels = [label for label, size in zip(label_order, sizes) if size > 0]
    filtered_sizes = [size for size in sizes if size > 0]
    filtered_colors = []
    for label in filtered_labels:
        if label == 'H':
            filtered_colors.append('gold')
        elif label == 'E':
            filtered_colors.append('skyblue')
        elif label == 'C':
            filtered_colors.append('lightgreen')

    plt.figure(figsize=(5, 5))
    plt.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', colors=filtered_colors)
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

def clean_old_graphs(current_uuid):
    """
    Deletes all graph files in assets folder that are not associated with the current UUID.
    """
    os.makedirs(ASSETS_FOLDER, exist_ok=True)

    for filename in os.listdir(ASSETS_FOLDER):
        if filename.startswith("structure_") or filename.startswith("pie_chart_") or filename.startswith("bar_chart_"):
            # Example filename: structure_1234abcd.png
            if current_uuid not in filename:
                try:
                    file_path = os.path.join(ASSETS_FOLDER, filename)
                    os.remove(file_path)
                    print(f"Deleted old graph: {filename}")
                except Exception as e:
                    print(f"Failed to delete {filename}: {e}")
