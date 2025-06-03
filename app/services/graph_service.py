# app/services/graph_service.py
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import os
matplotlib.use("Agg")

ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'assets')

def generate_structure_dot_plot(sequence, prediction_uuid):
    folder_path = os.path.join(ASSETS_FOLDER, prediction_uuid)
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, "structure.png")

    plt.figure(figsize=(len(sequence) // 2, 3))
    colors = {'H': 'gold', 'E': 'skyblue', 'C': 'lightgreen'}
    x = range(len(sequence))
    y = [0] * len(sequence)
    c = [colors.get(label, 'gray') for label in sequence]
    
    plt.scatter(x, y, c=c, s=100, edgecolors='black')
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def generate_pie_chart(sequence, prediction_uuid):
    from collections import Counter
    folder_path = os.path.join(ASSETS_FOLDER, prediction_uuid)
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, "pie_chart.png")

    counts = Counter(sequence)
    label_order = ['H', 'E', 'C']
    sizes = [counts.get(label, 0) for label in label_order]

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

def generate_bar_chart(sequence, database_hec_avg, prediction_uuid):
    from collections import Counter
    folder_path = os.path.join(ASSETS_FOLDER, prediction_uuid)
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, "bar_chart.png")

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

def delete_prediction_graphs(prediction_uuid):
    """Delete the prediction folder for the given UUID"""
    folder_path = os.path.join(ASSETS_FOLDER, prediction_uuid)
    if os.path.exists(folder_path):
        import shutil
        shutil.rmtree(folder_path)
        print(f"Deleted graphs folder: {folder_path}")
