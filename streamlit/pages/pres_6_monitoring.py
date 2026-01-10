import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Project Status (5)")
    st.markdown("""
    #### (5) Monitoring & Maintenance

    **What is the use of 'Prometheus'?**   
    - Collection of system and application metrics via HTTP endpoints   
    - Time-series storage for performance and health monitoring   
    - Basis for alerting and operational observability

    **What is the use of 'Grafana'?**   
    - Visualization of metrics from Prometheus and other data sources   
    - Interactive dashboards for infrastructure, application and model monitoring   
    - Support for trend analysis and anomaly inspection

    **What is the use of 'Node-exporter'?**   
    - Centralized aggregation of application and service logs   
    - Lightweight log indexing optimized for metric correlation   
    - Integrated log exploration within Grafana dashboards  

    **How we used these monitoring tools?**   
    - Prometheus --> scraping metrics (application + model)
    - Grafana --> visualizing dashboards from scraped data
    - 'dashboards' as IaC (see slide 'on-going') 
    - Node-exporter --> infrastructure monitoring
    
    ---

    **Live Demos**
    """)

    url_graf = "https://bookish-space-train-v6r9vrjvrjj9fwqwp-3000.app.github.dev/"
    url_prom = "https://bookish-space-train-v6r9vrjvrjj9fwqwp-9090.app.github.dev/"
    
    if st.session_state.monitoring:
        st.link_button("Prometheus UI", 
                        url_prom)
        st.link_button("Grafana UI", 
                        url_graf)

    else:
        st.warning("Monitoring tools are not yet deployed.", 
                icon="⚠️")


    # Prometheus
    # Prometheus ist ein zeitreihenbasiertes Monitoring-System, das Metriken über HTTP-Endpunkte sammelt und speichert.
    # Hier dient Prometheus zur Überwachung von API-Zugriffen, Laufzeiten und Systemzuständen und bildet die Grundlage für observability-orientiertes Debugging.

    # Loki
    # Loki ist ein log-zentriertes Aggregationssystem, das Logs effizient speichert und eng mit Grafana integriert ist.
    # Es ermöglicht die korrelierte Analyse von Logs und Metriken, ohne komplexe Volltextindizierung wie bei klassischen Log-Systemen.

    # Grafana
    # Grafana ist ein Visualisierungs- und Dashboard-Tool für Metriken aus verschiedenen Datenquellen (z. B. Prometheus).
    # Im Projekt wird Grafana verwendet, um System- und Modellmetriken übersichtlich darzustellen und Trends oder Anomalien visuell zu analysieren.

    