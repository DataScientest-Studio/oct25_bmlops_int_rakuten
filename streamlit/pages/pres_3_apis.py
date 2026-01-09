import streamlit as st
from pathlib import Path
import requests
etl_trigger_URL = "http://127.0.0.1:8001/etl/trigger"
def show():
    st.header("FastAPI")
    st.subheader("General Purpose")
    st.markdown("""
    - Python framework for quickly building web APIs   
    - Lightweight HTTP interface   
    - Decouples UI from orchestration
    """)
     
    ## 
    # col1, col2, col3 = st.columns(3, border=True)
    
    # Bsp.-Dateien für Testzwecke
    img_etl_trigger = Path("src/screenshots/etl_trigger.png")
    img_training = Path("src/screenshots/training.png")
    img_recos = Path("src/screenshots/recommend.png")
    code = Path("src/test.py").read_text(encoding="utf-8")
    st.subheader("Endpoints")
    with st.expander("trigger 'etl-pipeline'"):
        with st.popover("ETL-trigger"):
            st.image(str(img_etl_trigger), caption="ETL-trigger")

        st.divider()

        with st.expander("Code"):
            st.code(code, language="python")
        
        st.divider()
       
        if st.button("trigger API call", key="etl"):
            try:
        # POST request an FastAPI
                resp = requests.post(etl_trigger_URL)
                if resp.status_code == 200:
                    st.success("Pipeline erfolgreich gestartet!")
                else:
                    st.error(f"Fehler beim Starten: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.error(f"API-Call fehlgeschlagen: {e}")
       
    
    with st.expander("trigger 'create similarity matrtix'"):
        with st.popover("training trigger"):
            st.image(str(img_training), caption="training trigger")

        st.divider()

        with st.expander("Code"):
            st.code(code, language="python")
        
        st.divider()
       
        if st.button("trigger API call", key="SimMatrix"):
            st.write("add LINK to Airflow")
        else:
            st.write()
    
    with st.expander("ask for recommendations"):
        with st.popover("recommendations"):
            st.image(str(img_recos), caption="recommendations")

        st.divider()

        with st.expander("Code"):
            st.code(code, language="python")
        
        st.divider()
       
        if st.button("trigger API call", key="Recos"):
            st.write("add LINK to Airflow")
        else:
            st.write()
