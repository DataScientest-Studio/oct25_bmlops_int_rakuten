import streamlit as st
import sys
from pathlib import Path

from pages import (pres_0_home, pres_1_intro , pres_2_pipelines, pres_3_apis,
                    pres_4_mlflow, pres_5_docker, pres_6_monitoring, 
                    pres_7_conclusion) 

# configuration
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

# === Section 1: Project Presentation ===
st.sidebar.markdown("#### 🎥 Project Presentation")      
presentation = st.sidebar.radio(
    "Chapter:",
    options=[
        "🏠 Home",
        "🧭 Introduction",
        "🛠️ Pipeline & Airflow",
        "🔌 APIs",
        "🧪 MLflow",
        "📦 Docker",
        "📡 Monitoring",
        "🏁 Conclusion",
            ],
    key="presentation",         
    index=0,
    args=("presentation",)
    )


PAGES_PRESENTATION = {
    "🏠 Home": pres_0_home.show,
    "🧭 Introduction": pres_1_intro.show,
    "🛠️ Pipeline & Airflow": pres_2_pipelines.show,
    "🔌 APIs": pres_3_apis.show,
    "🧪 MLflow": pres_4_mlflow.show,
    "📦 Docker": pres_5_docker.show,
    "📡 Monitoring": pres_6_monitoring.show,
    "🏁 Conclusion": pres_7_conclusion.show
            }

PAGES_PRESENTATION[presentation]()


