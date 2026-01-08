import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Project Status (4)")
    st.markdown("""
    #### (4) Docker
    
    Docker
    Docker ermöglicht die Containerisierung von Anwendungen, d. h. 
    Software wird inklusive aller Abhängigkeiten in isolierten, 
    reproduzierbaren Laufzeitumgebungen ausgeführt.
    Im Projekt wird Docker genutzt, um API, Streamlit-App und Infrastrukturkomponenten 
    konsistent und portabel zu betreiben.

    Docker

Containerized execution of services and applications

Reproducible runtime environments across development and deployment

Isolation of dependencies for API, UI, and infrastructure components
    
    """)