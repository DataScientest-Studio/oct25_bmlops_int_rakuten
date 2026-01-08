import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Project Status (1)")
    st.markdown("""
    #### (1) Pipelines and orchestration
    

    MongoDB
    MongoDB ist eine dokumentenorientierte NoSQL-Datenbank, die strukturierte und 
    semi-strukturierte Daten flexibel speichert. Im Projekt eignet sie sich insbesondere 
    für Metadaten, Zwischenergebnisse und nicht-relationale Artefakte, die sich 
    dynamisch entwickeln.
    - Flexible storage for document-based and semi-structured data   
    - Persistence of metadata, intermediate results, and artifacts   
    - Suitable for evolving schemas and non-relational workloads

    Airflow
    - Orchestrates data preprocessing and feature pipelines  
    - Ensures reproducibility and traceability   
    - Handles scheduling and retries
    
    """)
     
    ## 
    col1, col2, col3 = st.columns(3, border=True)

    img = Path("static files/resnet.png")
    code = Path("src/test.py").read_text(encoding="utf-8")

    with col1:
        st.markdown("""
        #### ETL (extract - transform - load) 
        """)
        
        st.divider()
        
        with st.popover("Graph"):
            st.image(img)

        st.divider()
       
        with st.popover("DAG"):
            st.code(code, language="python")
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 FileSensor + API call
        
        [ADD SHOWCASE MOMENT "FileSensor" 
        + LINK TO AIRFLOW (st.link_button(name, url))]
        """)
    
    with col2:
        st.markdown("""
        ### Create simmilarity matrtix
        """)
        
        st.divider()
        
        with st.popover("Graph"):
            st.image(img)

        st.divider()
       
        with st.popover("DAG"):
            st.code(code, language="python")
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 FileSensor + API call
        """)
    
    with col3:
        st.markdown("""
        ### Make recommendations 
        """)
        
        st.divider()
        
        with st.popover("Graph"):
            st.image(img)
        
        st.divider()
       
        with st.popover("DAG"):
            st.code(code, language="python")
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 FileSensor + API call
        """)