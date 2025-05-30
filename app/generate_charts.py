import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

# Simpan di folder assets
os.makedirs("assets", exist_ok=True)

def save_charts_seaborn():
    # === PIE CHART (masih pakai matplotlib karena seaborn gak support pie) ===
    labels = ['Helix', 'Sheet', 'Coil']
    predicted = [60, 30, 10]
    colors = ['#FFC107', '#065D30', '#3F51B5']

    plt.figure(figsize=(4, 4))
    plt.pie(predicted, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("Predicted Protein Structure Distribution")
    plt.tight_layout()
    plt.savefig("assets/pie_chart.png")
    plt.close()

    # === BAR CHART pakai seaborn ===
    data = pd.DataFrame({
        'Structure': ['Helix', 'Sheet', 'Coil'],
        'Predicted': [60, 30, 10],
        'Known': [50, 40, 10]
    })

    # Long format biar seaborn bisa handle
    df_long = pd.melt(data, id_vars='Structure', var_name='Type', value_name='Value')

    plt.figure(figsize=(6, 4))
    sns.barplot(data=df_long, x='Structure', y='Value', hue='Type', palette='Set2')
    plt.title("Comparison with Known Protein Data")
    plt.tight_layout()
    plt.savefig("assets/bar_chart.png")
    plt.close()

if __name__ == "__main__":
    save_charts_seaborn()
