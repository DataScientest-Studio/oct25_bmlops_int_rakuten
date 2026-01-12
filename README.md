# Rakuten E-Commerce Product Classification (Multimodal)

Cataloging products based on heterogeneous data sources (text and images) is a core task in modern e-commerce systems. Accurate product classification enables downstream applications such as recommendation systems, personalized search, and catalog quality control.

This project addresses a **multimodal classification problem**: predicting the product type code using **textual information** (product designation and description) and **visual information** (product images).

---

## Data

The dataset is publicly available as part of the challenge and can be accessed here:  
🔗 https://challengedata.ens.fr/challenges/35

**Dataset characteristics**
- ~99,000 product entries
- ">1,000 product classes (highly imbalanced)"
- Text data: ~60 MB
- Image data: ~2.2 GB
- Noisy real-world e-commerce data

The dataset reflects realistic challenges such as class imbalance, heterogeneous text quality, and varying image resolution.

---

## Problem Framing & Approach

The task is formulated as a **supervised multi-class classification problem**.

High-level workflow:
1. **Data ingestion & validation**
2. **Text preprocessing & embedding**
3. **Image preprocessing & feature extraction**
4. **Model training**
   - text-only baseline
   - image-only baseline
   - multimodal fusion models
5. **Evaluation & error analysis**
6. **Interactive exploration via Streamlit**

The project deliberately emphasizes **model interpretability, reproducibility, and modular design**, rather than pure leaderboard optimization.

---

## 📁 Project structure

<style>
.comment {
  margin-left: 12px;
  color: #666;
  font-style: italic;
}
</style>

<body>
	<p>
	├── <a href="./airflow/">airflow</a><span class="comment"> — Workflow orchestration (ETL, scheduling)</span><br>
	│   ├── <a href="./airflow/dags/">dags</a><br>
	│   ├── <a href="./airflow/logs/">logs</a><br>
	│   └── <a href="./airflow/plugins/">plugins</a><br>
	├── <a href="./data/">data</a><br>
	│   ├── <a href="./data/dags/">dags</a><br>
	│   ├── <a href="./data/logs/">logs</a><br>
	│   └── <a href="./data/plugins/">plugins</a><br>	
	├── <a href="./fastapi/">fastapi</a><br>
	├── <a href="./logs/">logs</a><br>
	├── <a href="./mlflow/">mlflow</a><br>
	│   ├── <a href="./mlflow/artifacts/">artifacts</a><br>
	│   └── <a href="./mlflow/data/">data</a><br>
	│   &nbsp;&nbsp;&nbsp; └── <a href="./mlflow/data/artifacts/">artifacts</a><br>
	├── <a href="./monitoring/">monitoring</a><br>
	│   ├── <a href="./monitoring/grafana/">grafana</a><br>
	│   │   ├── <a href="./monitoring/grafana/dashboards/">dashboards</a><br>
	│   │   └── <a href="./monitoring/grafana/provisioning/">provisioning</a><br>
	│   │   &nbsp;&nbsp;&nbsp; ├── <a href="./monitoring/grafana/provisioning/dashboards/">dashboards</a><br>
	│   │   &nbsp;&nbsp;&nbsp; └── <a href="./monitoring/grafana/provisioning/data_sources/">data_sources</a><br>
	│   └── <a href="./monitoring/prometheus/">prometheus</a><br>
	│   &nbsp;&nbsp;&nbsp; └── <a href="./monitoring/prometheus/rules/">rules</a><br>
	├── <a href="./scripts/">scripts</a><br>
	├── <a href="./src/">src</a><span class="comment"> — contains Python scripts</span><br>
	│   └── <a href="./src/utils/">utils</a><span class="comment"> — contains py-files of helper functions, class definitions,...</span><br>
	├── <a href="./streamlit/">streamlit</a><span class="comment"> — frontend: presentation / live demo of project</span><br>
	│   ├── <a href="./streamlit/logs/">logs</a><span class="comment"> — log files used for streamlit app</span><br>
	│   ├── <a href="./streamlit/pages/">pages</a><span class="comment"> — pages from streamlit app</span><br>
	│   ├── <a href="./streamlit/src/">src</a><span class="comment"> — contains Python scripts and a py-file of utility functions</span><br>
	│   │   ├── <a href="./streamlit/src/codes/">codes</a><br>
	│   │   └── <a href="./streamlit/src/screenshots/">screenshots</a><br>
	│   └── <a href="./streamlit/static_files/">static_files</a><br>
	└── <a href="./tests/">tests</a><br>
<br>
</p>

The repository follows the principles of the *cookiecutter data science* template, with additional components for MLOps experimentation and interactive visualization.

--------

## Key Components    

- **`Makefile`**   
  shortened commands for often executed files 

- **`notebooks/`**  
  Exploratory data analysis, feature engineering, and model experiments.

- **`scripts/`** 
  Reusable shell scripts
  
- **`streamlit/`**  
  Interactive application to explore the dataset, model behavior, and results.

- **`src/`**  
  Reusable Python modules for preprocessing, training, and evaluation.

--------

## Project Information
## Prerequisites
+ python 3.11.x
+ Git
+ Python venv

--------

## Setup Guide (Streamlit app)

```bash
# (1) Activate venv (for Linux and macOS)
source .venv/bin/activate

# (2) Install the basically required packages
pip install -r requirements.txt

# (3) Run the streamlit application:
streamlit run streamlit/app.py

# (4) Open your browser and navigate to `http://localhost:8501` to view the application.
```

## Setup Guide (Project)

```bash
# (1) activate virtual environment
source .venv/bin/activate

# (2-A) install core dependencies
pip install -r requirements.txt

# (2-B) install mlops dependencies
pip install -r requirements-mlops.txt

# (2-C) install mlops and heavy dependencies
pip install -r requirements-heavy.txt

# (2-D) install all dependencies (mlops, heavy and dev)
pip install -r requirements-dev.txt
```

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
