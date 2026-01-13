import streamlit as st
from pathlib import Path

from src.utils import live_command_demo

LOGS = Path("/workspaces/oct25_bmlops_int_rakuten/streamlit/logs")
LOGS.mkdir(parents=True, exist_ok=True)
    
log_api = LOGS / "build_api"
# log_monitoring = LOGS / "build_monitoring"

def show():
    st.header("📡 Monitoring & Maintenance")
    st.markdown("""
    
    **What is the use of 'Prometheus'?**   
    - Collection of system and application metrics via HTTP endpoints   
    - Time-series storage for on-going monitoring of infrastructure, application and model    
    - Basis for alerting and operational observability

    **What is the use of 'Grafana'?**   
    - Visualization of metrics from Prometheus and other data sources   
    - Interactive dashboards for monitoring data   
    - Support for trend analysis and anomaly inspection   
    - dashboards = IaC: portable/exchangable, versionable, less human errors,... 


    **What is the use of 'Node-exporter'?**   
    - Centralized aggregation of application and service logs   
    - Lightweight log indexing optimized for metric correlation   
    - Integrated log exploration within Grafana dashboards  

    **How we used these monitoring tools?**   
    - Prometheus --> scraping metrics (infrastructure, application, model)
    - Grafana --> visualizing dashboards from scraped data
    - Node-exporter --> infrastructure monitoring
    
    ---

    ⚡ **Live Demos**
    """)
    url_graf = "https://localhost:3000"
    url_prom = "https://localhost:9090"
    
    top_left, top_right = st.columns(2)
    left, middle, right_1, right_2 = st.columns(4)

    status = top_left.status("Waiting...", 
                        state="complete",
                        expanded=True)
    
    with top_right.popover("log 'API'"):
        st.write()
        
    # if st.session_state.monitoring_running:
    left.link_button("Prometheus UI", 
                    url_prom,
                    width="stretch")
    middle.link_button("Grafana UI", 
                    url_graf,
                    width="stretch")

    # else:
    #     st.warning("Monitoring tools are not yet deployed.", 
    #             icon="⚠️")

    if right_1.button(
                "Build API container",
                width="stretch",
                key="api_container"                
                    ):
        
        cmd = ["make", "api_docker"]

        status.update(label="Buidling API container...", state="running")

        exit_code = live_command_demo(cmd, log_api, mode="a")

        if exit_code == 0:
            status.update(
                label="Buidling API container finished successfully.", 
                state="complete",
                expanded=False
                )
            # st.success("Building API containers finished successfully.")
        else:
            status.update(
                label=f"Buidling API container failed (exit code {exit_code}).", 
                state="error",
                expanded=True
                )

    if right_2.button(
            "generate API traffic", 
            width="stretch", 
            key="traffic_gen"
                ):

        cmd = ["make", "traffic"]

        status.update(label="Generating traffic on API...", state="running")

        exit_code = live_command_demo(cmd, log_api, mode="a")       # file_mode

        if exit_code == 0:
            status.update(
                label="Generating traffic on API finished successfully.", 
                state="complete",
                expanded=False
                )
            # st.success("Building API containers finished successfully.")
        else:
            status.update(
                label=f"Generating traffic on API failed (exit code {exit_code}).", 
                state="error",
                expanded=True,
                )
            # st.error(f"Building MLflow containers failed (exit code {exit_code}).")

        # st.session_state.build_running = False


    # Prometheus
    # Prometheus ist ein zeitreihenbasiertes Monitoring-System, das Metriken über HTTP-Endpunkte sammelt und speichert.
    # Hier dient Prometheus zur Überwachung von API-Zugriffen, Laufzeiten und Systemzuständen und bildet die Grundlage für observability-orientiertes Debugging.

    # Loki
    # Loki ist ein log-zentriertes Aggregationssystem, das Logs effizient speichert und eng mit Grafana integriert ist.
    # Es ermöglicht die korrelierte Analyse von Logs und Metriken, ohne komplexe Volltextindizierung wie bei klassischen Log-Systemen.

    # Grafana
    # Grafana ist ein Visualisierungs- und Dashboard-Tool für Metriken aus verschiedenen Datenquellen (z. B. Prometheus).
    # Im Projekt wird Grafana verwendet, um System- und Modellmetriken übersichtlich darzustellen und Trends oder Anomalien visuell zu analysieren.

    