# Rakuten E-Commerce Product Classification (Multimodal)

Cataloging products based on heterogeneous data sources (text and images) is a core task in modern e-commerce systems. Accurate product classification enables downstream applications such as recommendation systems, personalized search, and catalog quality control.

This project addresses a **multimodal classification problem**: predicting the product type code using **textual information** (product designation and description) and **visual information** (product images).

The work is based on the *Rakuten France Multimodal Product Data Classification* challenge.

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

## Project Organization

> ⚠️ *Structure is under active refactoring.*

A browsable HTML overview of the current project structure is available here:

<p align="left">
  <a href="static files/tree_commented.html">📁 Full project structure (HTML)</a>
</p>

The repository follows the principles of the *cookiecutter data science* template, with additional components for MLOps experimentation and interactive visualization.

---

## Key Components

- **`notebooks/`**  
  Exploratory data analysis, feature engineering, and model experiments.

- **`src/`**  
  Reusable Python modules for preprocessing, training, and evaluation.

- **`streamlit/`**  
  Interactive application to explore the dataset, model behavior, and results.

- **`reports/`**  
  Consolidated project report and intermediate experiment summaries.

---

## Software Architecture Overview
### software descriptions
- Docker: containerized execution of services
- Prometheus & Grafana: metrics collection and visualization
- Loki: centralized log aggregation
- MongoDB: flexible storage for metadata and artifacts

### user focused  
User / Data
        │
        ▼
FastAPI Service (Pipeline trigger)
      (A) ETL                                   (B) 'training' / recommendation                   (C) ??
        │                                                    │                                                  |
        ▼                                                    ▼                                                  ▼
Airflow (Data processing & orchestration)       ('Training' /  Recommendation & orchestration)     
        |                                                    │
        │                                                    │
        ▼                                                    ▼
Feature Pipeline                                 Training / Recommendation Pipelines
        │                                                    |
        ▼                                                    ▼
    - Data storage (MongoDB)                    - Experiment tracking (MLflow)
    - Application & Infrastructure Monitoring (Prometheus, Grafana, Node-explorer)
      
      
## Prerequisites

- Python **3.11.x**
- Git
- Virtual environment support (`venv`)
- (Optional) Docker for containerized execution

---

## Setup Guide

```bash
# (1) create & activate virtual environment
uv init
source .venv/bin/activate

# (2-A) install core dependencies
make setup         # then 'enter' in shell

# (2-B) install other dependency group/-s
make setup         # then enter 'mlops', 'dev', 'heavy' or 'all' + 'enter' in shell
```

see [pyproject.toml](pyproject.toml) for details)
