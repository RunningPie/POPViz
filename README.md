
# 📚 POPViz - Protein Structure Predictor

POPViz (Protein Prediction and Visualization) is a modern, interactive platform that allows users to predict secondary protein structures from amino acid sequences.
Built with **Flet** for the front-end and **TensorFlow** for the back-end ML model, it offers an intuitive interface for researchers, students, and bioinformaticians.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" />
  <img src="https://img.shields.io/badge/Flet-UI-success" />
  <img src="https://img.shields.io/badge/TensorFlow-2.19-orange" />
  <img src="https://img.shields.io/badge/Docker-Ready-informational" />
</p>

---

# 🚀 Key Features

- 🧬 **Protein Secondary Structure Prediction**: Predicts secondary structures (Helix, Sheet, Coil) from input sequences.
- 📊 **Beautiful Visualizations**:
  - Dot plot of structure
  - Pie chart of structure distribution
  - Bar chart comparison with known databases
- 📖 **History Management**:
  - View past predictions
  - Download results as **PDF**
- 🖥️ **Desktop App Mode** (Local Run)
- 🌐 **Web App Mode** (Docker Run)
- 🐳 **Docker-Ready**: Easily containerized for portability and reproducibility.

---

# 📦 Project Structure

```
POPViz/
├── app/                  # Main application source code
│   ├── main.py            # Entry point
│   ├── pages/             # Flet Pages (input, history, result)
│   ├── services/          # Prediction and graph services
│   └── assets/            # Static assets (graphs generated here)
├── ML/                    # ML models, scaler, encoder
├── requirements.txt       # Python dependencies
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Docker Compose config
├── README.md               # Project documentation (this file)
└── .dockerignore           # Docker ignore list
```

---

# 🚀 Why POPViz?

### ✅ Predict with Confidence
Use trained deep learning models to predict the secondary structure of proteins — critical for understanding function and interactions.

### 🎨 Visualize Complex Data Easily
Graphical representation of predicted structures, insightful statistical charts, and downloadable reports.

### 📜 Maintain Your Work
History management ensures you never lose your past predictions.

### 🐳 Portable and Reproducible
Thanks to Docker, you can run this anywhere — no more "it works on my machine" problems.

### 🖥️ Flexible Deployment
- Local Desktop App experience (GUI-based).
- Web App inside Docker for easy deployment across systems.

---

# ⚙️ How to Run This Project

## 🔧 1. Local Development (Desktop App)

> **Requirements**:
> - Python 3.12+
> - Conda environment highly recommended to ensure correct Python version.

```bash
# Clone the repository
git clone <your-repo-url>
cd POPViz

# Create and activate conda environment (Recommended)
conda create -n popviz python=3.12
conda activate popviz

# Install dependencies
pip install -r requirements.txt

# Run the app
python app/main.py
```

🖥️ The app will open in **Desktop App Mode** automatically.

---

## 🐳 2. Docker Deployment (Web App Mode)

> **Requirements**:
> - Docker
> - Docker Compose

```bash
# In the project root (POPViz/)
docker-compose up --build
```

🖥️ Open your browser and go to:
```
http://localhost:8550
```

✅ Docker will **automatically detect** it’s inside a container and run the app in **Web Browser Mode**.

⚠️ It takes approximately 5 minutes for the docker image to build because of tensorflow dependency which is ~650 MB in size

---

# 🧩 Environment Detection

- Local Environment ➔ **Desktop App** (Flet Native Window)
- Docker Environment ➔ **Web App** (Flet Web, Browser UI)

We achieve this via the environment variable:
```yaml
environment:
  - RUNNING_IN_DOCKER=1
```
inside `docker-compose.yml`.

---

# 📝 Notes

- Default port for Web App: `8550`
- Docker will bind mount your `app/` and `ML/` folders for live updates.
- History and graphs are stored persistently inside the `app/assets/` folder.
- TensorFlow 2.19.0 is used — make sure you have a decent machine for faster predictions.

---

# 🌟 Future Enhancements

- 🧬 Export predictions as FASTA format.
- 📊 More advanced statistical analysis (e.g., Ramachandran plots).
- 🌐 Online deployment (Heroku, AWS, GCP).
- 🛡️ User Authentication (for multi-user history management).

---

# ❤️ Contributors

- 👩‍💻 [Dama D. Daliman](https://github.com/RunningPie) as Software Engineer
- 👩‍💻 [Naomi Pricilla Agustine](https://github.com/naomipricillaa) as UI UX Designer
- 👩‍💻 [Micky Valentino](https://github.com/MickyV18) as AI/ML Engineer

- 🙏 Thanks to the open-source community: [TensorFlow](https://tensorflow.org), [Flet](https://flet.dev)

---

# 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

# 🎯 Ready to Predict?
Clone, run, and dive into the beautiful world of proteins! 🧬✨
