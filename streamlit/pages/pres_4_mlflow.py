import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Project Status (3)")
    st.markdown("""
    #### (3) Experiment tracking 
    
    **MLflow**   
    - Offline experiments (notebooks & scripts)   
    - Model training and evaluation   
    - Artifact generation (metrics, embeddings, reports)
    """)
    img1 = Path("src/screenshots/mlflow1.png")
    img2 = Path("src/screenshots/mlflow2.png")
    st.image(str(img1), caption="MLflow Dashboard 1")
    st.image(str(img2), caption="MLflow Dashboard 2")