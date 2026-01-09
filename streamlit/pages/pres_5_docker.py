import streamlit as st
import os
from pathlib import Path

# from src.utils import live_command_demo

import time
import subprocess

def live_command_demo(cmd, log_name, mode="a"): # , live=True):
    placeholder = st.empty()
    
    # if mode == "new":
    #     edit_mode = "a"
    # elif mode == "write":
    #     edit_mode = "w"
    # elif mode == "new":
    log_file = Path(f"{log_name}.log")
    #     edit_mode = ""

    with open(log_file, mode) as log:
        process = subprocess.Popen(
            cmd,
            # ["make", "api_docker"],
            stdout=log, # open("build_apis.log", "w"),
            stderr=subprocess.STDOUT,
            text=True
    )

    # if live:
    while True:
#         for _ in range(60):  # Demo-Zeitfenster
        if log_file.exists():
            placeholder.code(log_file.read_text(), 
                            language="text")
        else:
            placeholder.info("Waiting for log output...")
        exit_code = process.poll()

        if exit_code is not None:
            break

        time.sleep(1)

    # if error_mark:
    #     lines = log_file.read_text().splitlines()
    #     errors = [l for l in lines if "ERROR" in l or "FAILED" in l]
    #     if errors:
    #         st.code("\n".join(errors), language="text")

    return exit_code

make_extract = Path("/workspaces/oct25_bmlops_int_rakuten/streamlit/src/makefile_extract.py").read_text(encoding="utf-8")

docker_compose_api = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.api.yaml").read_text(encoding="utf-8")
docker_file_api = Path("/workspaces/oct25_bmlops_int_rakuten/fastapi/Dockerfile").read_text(encoding="utf-8")
docker_airflow = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.airflow.yaml").read_text(encoding="utf-8")
docker_monitoring = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.monitoring.yaml").read_text(encoding="utf-8")
docker_compose_ml = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.ml.yaml").read_text(encoding="utf-8")
docker_file_ml = Path("/workspaces/oct25_bmlops_int_rakuten/mlflow/Dockerfile").read_text(encoding="utf-8")

def show():
    st.header("📑 Project Status (4)")
    st.markdown("""
    #### (4) Docker and microservice architecture
    
    **What is the use of 'Docker'?**   
    - Containerized execution of services and applications   
    - Reproducible runtime environments across development and deployment   
    - Isolation of dependencies for API, UI, and other infrastructure components
    - Allows a microservice architecture and portability (**DockerHub**)

    --- 

    **How we used Docker?**
    - one docker-compose.yaml per 'microservice' and a Dockerfile if necessary   
    """)
   
    with st.expander("Docker-composes and Dockerfiles"):
        # col1, col2, col3, col4 = st.columns(4, border=True)

        with st.container(border=True):
            st.markdown("""
            **Docker 'Airflow'** covers:   
            - Airflow (incl. init, scheduler, webserver)   
            - PostgreSQL  
            """)
            
            with st.popover("**docker-compose.airflow.yaml**"):
                st.code(docker_airflow, language="python")


        with st.container(border=True):
            st.markdown("""
            **Docker 'APIs'** covers:   
            - FastAPI   
            - Streamlit  
            """)
            
            with st.popover("**docker-compose.api.yaml**"):
                st.code(docker_compose_api, language="python")
            
            with st.popover("**Dockerfile (API)**"):
                st.code(docker_file_api, language="python")
        
        with st.container(border=True):
            st.markdown("""
            **Docker 'ML'** covers:   
            - MLflow,   
            - SQLite/PostgreSQL if necessary,   
            - prospectively, W&B or similar 
            
            """)
            with st.popover("**docker-compose.ml.yaml**"):
                st.code(docker_compose_ml, language="python")
            
            with st.popover("**Dockerfile (MLflow)**"):
                st.code(docker_file_ml, language="python")
        
        with st.container(border=True):
            st.markdown("""
            **Docker 'Monitoring'** covers:   
            - Prometheus   
            - Grafana   
            - Node-explorer   
            - Promtail (*not yet fully integrated*)   
            - Loki (*not yet fully integrated*)
            
            """)
            with st.popover("**docker-compose.monitoring.yaml**"):
                st.code(docker_monitoring, language="python")
    
    st.markdown("""
    - automation by using Makefile   
    **-->** same project by default --> no network mismatches possible

    """)
    with st.popover("Extract from **Makefile**", width="stretch"):
        st.code(make_extract, language="python")

    st.markdown("""
    ---

    **Live Demos**
    """)
    # Docker ermöglicht die Containerisierung von Anwendungen, d. h. 
    # Software wird inklusive aller Abhängigkeiten in isolierten, 
    # reproduzierbaren Laufzeitumgebungen ausgeführt.
    # Im Projekt wird Docker genutzt, um API, Streamlit-App und Infrastrukturkomponenten 
    # konsistent und portabel zu betreiben.

    LOGS = Path("/workspaces/oct25_bmlops_int_rakuten/streamlit/logs")
    LOGS.mkdir(parents=True, exist_ok=True)
    
    log_apis = LOGS / "build_apis"
    log_monitoring = LOGS / "build_monitoring"

    left, middle, right = st.columns(3)

    
    status = st.status("Please, choose a button...", 
                        state=None,
                        expanded=True)

    if left.button("build APIs", width="stretch", key="api"):
        cmd = ["make", "api_docker"]

        status.update("Running API build...", state="running")

        exit_code = live_command_demo(cmd, log_apis)

        if exit_code == 0:
            status.update(label="Build finished", state="complete")
            st.success("Building API containers finished successfully.")
        else:
            status.update(label="Build failed", state="error")
            st.error(f"Building API containers failed (exit code {exit_code}).")

    if middle.button("build monitoring", width="stretch", key="monitoring"):
        cmd = ["make", "api_monitoring"]

        status.update("Running monitoring build...", state="running")
        exit_code = live_command_demo(cmd, log_apis)

        if exit_code == 0:
            status.update(label="Build finished", state="complete")
            st.success("Building monitoring containers finished successfully.")
        else:
            status.update(label="Build failed", state="failed")
            st.error(f"Building monitoring containers failed (exit code {exit_code}).")

    if right.button("reset", type="tertiary", icon="🔥"):
        status.upate("Status reset. choose a button...", state=None)

        # variante B
        # import logging

        # logging.basicConfig(
        #     filename="pipeline.log",
        #     level=logging.INFO,
        #     format="%(asctime)s | %(levelname)s | %(message)s",
        # )

        # logging.info("Pipeline started")

    # else:
    #     MAX_RETRIES = 10
    #     SLEEP_SECONDS = 1
    #     COUNT = 1
        
    #     while MAX_RETRIES >= COUNT:
    #         exit_code = process.poll()
    #         if exit_code is not None:
    #             break

    #         placeholder.info(f"Waiting for log file... (attempt {COUNT}/{MAX_RETRIES})")
    #         time.sleep(SLEEP_SECONDS)
    #         COUNT += 1

    #     for attempt in range(1, MAX_RETRIES + 1):
    #         if log_file.exists():
    #             placeholder.code(log_file.read_text(), language="text")
    #             break
    #         else:
    #             placeholder.info(f"Waiting for log file... (attempt {attempt}/{MAX_RETRIES})")
    #             time.sleep(SLEEP_SECONDS)
    #     else:
    #         placeholder.error("Log file did not appear.")
    #             # count+=1
    #         #     st.info("No log output yet.")
    #     # st.write("add LINK to Airflow")
    # else:
    #     st.write("")
    # st.divider()