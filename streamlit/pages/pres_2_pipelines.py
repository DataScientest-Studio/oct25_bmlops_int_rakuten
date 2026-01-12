import streamlit as st
from pathlib import Path

def show():

    st.header("🛠️ Pipeline and Orchestration with Airflow")
    st.subheader("Purposes")
    st.markdown("""
    - Orchestrates and automates data preprocessing and feature pipelines via DAGs
    - Handles scheduling and retries of ML processes 
    - Ensures reproducibility and traceability   
    """
    )
    #st.subheader("(2) Benefits")
    #st.markdown("""
    #- Workflows defined as code (Python) → easy to maintain and version
    #- Clear visualization of pipelines (DAGs) via web UI
    #- Strong error handling (retries, alerts, logging)   
    #- Integrates well with MLOps tools (e.g. MLflow, Docker)
    #"""
    #)

    ## 
    col1, col2 = st.columns(2, border=True)

    img_details_processing = Path("src/screenshots/details_processing.png")
    img_graph_processing = Path("src/screenshots/graph_processing.png")
    img_details_training = Path("src/screenshots/details_training.png")
    img_graph_training = Path("src/screenshots/graph_training.png")
    code1 = Path("src/codes/dag1.py").read_text(encoding="utf-8")
    code2 = Path("src/codes/dag2.py").read_text(encoding="utf-8")
    with col1:
        st.markdown("""
        #### ETL (extract - transform - load) 
        """)
        
        st.divider()
        
        with st.popover("Details"):
            st.image(str(img_details_processing), caption="ETL Details")

        st.divider()

        with st.popover("Graph"):
            st.image(str(img_graph_processing), caption="ETL Graph")

        st.divider()
       
        with st.popover("DAG"):
            st.code(code1, language="python")
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 API call
        """)
    
    with col2:
        st.markdown("""
        ### Create simmilarity matrtix
        """)
        
        st.divider()
        
        with st.popover("Details"):
            st.image(str(img_details_training), caption="Training Details")

        st.divider()

        with st.popover("Graph"):
            st.image(str(img_graph_training), caption="Training Graph")
       
       
        st.divider()
        with st.popover("DAG"):
            st.code(code2, language="python")
       
        st.divider()
        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 API call
        """)
    
    st.subheader("(3) Tasks")
    st.caption("wait_for_file")
    st.markdown("""
    - Collects raw data files (CSV or ZIP) from an input directory (data_input)
    - Moves the files to a centralized storage location (data lake)
    - Ensures that only supported file types are passed to downstream tasks   
    """
    )
    st.caption("run_fetch_files")
    st.markdown("""
    - Controls pipeline start with error and skip handling
    - Skips next task if no new data was found  
    """
    )
    st.caption("new_file_check")
    st.markdown("""
    - Compares newly ingested files (CSV/ZIP) with existing data
    - Detects whether the current data is already up-to-date or outdated
    - Returns signal if downstream tasks should run or not  
    """
    )
    st.caption("run_image_etl and run_text_general_etl")
    st.markdown("""
    - Extracting relevant data from CSV (texts) and ZIP (images)
    - Storing the information in a MongoDB collection  
    """
    )
    st.caption("run_image_embed and run_text_embed")
    st.markdown("""
    - Extracts data from MongoDB
    - Calculate Embeddings for texts (SentenceTransfomer) and images (CLIP-Model)  
    - Adding embeddings to MongoDB
    """
    )
    st.caption("train_knn (1)")
    st.markdown("""
    - Extracts embeddings from MongoDB and combines them 
    - Creates Similarity Matrix with KNN
    - Stores Mappings and Top-K-Neighbours locally
    - Logs Parameters in MLflow
    """
    )
    st.caption("train_knn (2)")
    st.markdown("""
    - Checks how well KNN neighbors match product categories
    - Computes an average category match score
    - Saves evaluation and logs metrics to MLflow
    """
    )