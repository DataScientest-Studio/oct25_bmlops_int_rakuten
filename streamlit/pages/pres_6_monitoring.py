import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Project Status (5)")
    st.markdown("""
    #### (5) Monitoring & Maintenance
  
    Prometheus
    Prometheus ist ein zeitreihenbasiertes Monitoring-System, das Metriken über HTTP-Endpunkte sammelt und speichert.
    Hier dient Prometheus zur Überwachung von API-Zugriffen, Laufzeiten und Systemzuständen und bildet die Grundlage für observability-orientiertes Debugging.

    Prometheus
    Collection of system and application metrics via HTTP endpoints
    Time-series storage for performance and health monitoring
    Basis for alerting and operational observability

    Grafana
    Grafana ist ein Visualisierungs- und Dashboard-Tool für Metriken aus verschiedenen Datenquellen (z. B. Prometheus).
    Im Projekt wird Grafana verwendet, um System- und Modellmetriken übersichtlich darzustellen und Trends oder Anomalien visuell zu analysieren.

    Grafana
    Visualization of metrics from Prometheus and other data sources
    Interactive dashboards for system and model monitoring
    Support for trend analysis and anomaly inspection

    Loki
    Loki ist ein log-zentriertes Aggregationssystem, das Logs effizient speichert und eng mit Grafana integriert ist.
    Es ermöglicht die korrelierte Analyse von Logs und Metriken, ohne komplexe Volltextindizierung wie bei klassischen Log-Systemen.

    Loki
    Centralized aggregation of application and service logs
    Lightweight log indexing optimized for metric correlation
    Integrated log exploration within Grafana dashboards  
    """)