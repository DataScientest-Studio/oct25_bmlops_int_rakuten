import streamlit as st
import os
from pathlib import Path
from datetime import datetime

from src.utils import live_command_demo

import time
import subprocess


make_extract = Path("/workspaces/oct25_bmlops_int_rakuten/streamlit/src/makefile_extract.py").read_text(encoding="utf-8")

docker_compose_api = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.api.yaml").read_text(encoding="utf-8")
docker_file_api = Path("/workspaces/oct25_bmlops_int_rakuten/fastapi/Dockerfile").read_text(encoding="utf-8")
docker_airflow = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.airflow.yaml").read_text(encoding="utf-8")
docker_monitoring = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.monitoring.yaml").read_text(encoding="utf-8")
docker_compose_ml = Path("/workspaces/oct25_bmlops_int_rakuten/docker-compose.ml.yaml").read_text(encoding="utf-8")
docker_file_ml = Path("/workspaces/oct25_bmlops_int_rakuten/mlflow/Dockerfile").read_text(encoding="utf-8")

def show():
    st.header("📦 Docker and microservice architecture")
    st.markdown("""
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
            
            with st.popover("ℹ️ **docker-compose.airflow.yaml**"):
                st.code(docker_airflow, language="python")


        with st.container(border=True):
            st.markdown("""
            **Docker 'APIs'** covers:   
            - FastAPI   
            - Streamlit  
            """)
            
            with st.popover("ℹ️ **docker-compose.api.yaml**"):
                st.code(docker_compose_api, language="python")
            
            with st.popover("ℹ️ **Dockerfile (API)**"):
                st.code(docker_file_api, language="python")
        
        with st.container(border=True):
            st.markdown("""
            **Docker 'ML'** covers:   
            - MLflow,   
            - SQLite/PostgreSQL if necessary,   
            - prospectively, W&B or similar 
            
            """)
            with st.popover("ℹ️ **docker-compose.ml.yaml**"):
                st.code(docker_compose_ml, language="python")
            
            with st.popover("ℹ️ **Dockerfile (MLflow)**"):
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
            with st.popover("ℹ️ **docker-compose.monitoring.yaml**"):
                st.code(docker_monitoring, language="python")
    
    st.markdown("""
    - automation by using Makefile   
    **-->** same project by default --> no network mismatches possible

    """)
    with st.popover("ℹ️ Extract from **Makefile**", width="stretch"):
        st.code(make_extract, language="python")

    st.markdown("""
    ---

    **⚡ Live Demos**
    """)
    # Docker ermöglicht die Containerisierung von Anwendungen, d. h. 
    # Software wird inklusive aller Abhängigkeiten in isolierten, 
    # reproduzierbaren Laufzeitumgebungen ausgeführt.
    # Im Projekt wird Docker genutzt, um API, Streamlit-App und Infrastrukturkomponenten 
    # konsistent und portabel zu betreiben.

    LOGS = Path("/workspaces/oct25_bmlops_int_rakuten/streamlit/logs")
    LOGS.mkdir(parents=True, exist_ok=True)
    
    log_ml = LOGS / "build_ml"
    log_monitoring = LOGS / "build_monitoring"
    log_docker = LOGS / "docker_status"

    # if "build_running" not in st.session_state:
    #     st.session_state.build_running = False

    if "monitoring_running" not in st.session_state:
        st.session_state.monitoring_running = False
    
    # if "build_ml" not in st.session_state:
    #     st.session_state.build_running = False
    
    top_left, top_middle, top_right = st.columns(3)
    bottom_left, bottom_middle, bottom_right = st.columns(3)

    status = st.status("Please, choose a button to build Docker containers...", 
                        state="complete",
                        expanded=True)

    # ------------
    # TOP ROW  
    # ------------ 
    # top right
    options_dict = {
        "append": "a",
        "write": "w"
    }
    sel = top_right.pills(
        "file edit mode",
        options = options_dict.keys(),
        # format_func=lambda option: options_dict[option],
        selection_mode="single",
        default="append"
    )

    file_mode = options_dict[sel]

    if top_left.button(
                "build MLflow", 
                width="stretch", 
                key="ml",
                # disabled=st.session_state.build_running
                ): # and not st.session_state.build_running:
        
        # st.session_state.build_running = True

        cmd = ["make", "ml_docker"]

        status.update(label="Running MLflow build...", state="running")


        exit_code = live_command_demo(cmd, log_ml, mode=file_mode)

        if exit_code == 0:
            status.update(
                label="Building MLflow containers finished successfully.", 
                state="complete",
                expanded=False
                )
            # st.success("Building API containers finished successfully.")
        else:
            status.update(
                label=f"Building MLflow containers failed (exit code {exit_code}).", 
                state="error",
                expanded=True,
                )
            st.error(f"Building MLflow containers failed (exit code {exit_code}).")

        # st.session_state.build_running = False

    if top_middle.button(
                    "build monitoring", 
                    width="stretch", 
                    key="monitoring",
                    # disabled=st.session_state.build_running
                    ): #  and not st.session_state.build_running:

        # st.session_state.build_running = True

        cmd = ["make", "monitoring_docker"]

        status.update(label="Running monitoring build...", state="running")
        exit_code = live_command_demo(cmd, log_monitoring, mode=file_mode)

        if exit_code == 0:
            status.update(
                label="Building monitoring containers finished successfully.", 
                state="complete",
                expanded=False
                )
        else:
            status.update(
                label=f"Building monitoring containers failed (exit code {exit_code}).", 
                state="error",
                expanded=True,
                )

        # st.session_state.build_running = False
        st.session_state.monitoring_running = True

    
    # ("reset", type="tertiary", icon="🔥"):
        # st.session_state.build_running = False
        # status.update(
        #         label="Status reset. choose a button...", 
        #         state="complete",
        #         expanded=False)

    # ------------
    # BOTTOM ROW  
    # ------------ 
    if bottom_left.button(
                "remove MLflow", 
                width="stretch", 
                key="ml_remove",
                # disabled=st.session_state.build_running
                ): #  and not st.session_state.build_running:
        
        # st.session_state.build_running = True

        cmd = ["make", "ml_stop"]

        status.update(label="Running MLflow removal...", state="running")

        exit_code = live_command_demo(cmd, log_ml, mode=file_mode)

        if exit_code == 0:
            status.update(
                label="Removing AMLflow containers finished successfully.", 
                state="complete",
                expanded=False
                )
            # st.success("Building API containers finished successfully.")
        else:
            status.update(
                label=f"Removing MLflow containers failed (exit code {exit_code}).", 
                state="error",
                expanded=True,
                )
            # st.error(f"Building API containers failed (exit code {exit_code}).")

        # st.session_state.build_running = False
        # st.session_state.api = False

    if bottom_middle.button(
                    "remove monitoring", 
                    width="stretch", 
                    key="monitoring_remove",
          #           disabled=st.session_state.build_running
                    ):

        # st.session_state.build_running = True

        cmd = ["make", "monitoring_stop"]

        status.update(label="Running monitoring removal...", state="running")
        exit_code = live_command_demo(cmd, log_monitoring, mode=file_mode)

        if exit_code == 0:
            status.update(
                label="Removing monitoring containers finished successfully.", 
                state="complete",
                expanded=False
                )
        else:
            status.update(
                label=f"Removing monitoring containers failed (exit code {exit_code}).", 
                state="error",
                expanded=True,
                )

        # st.session_state.build_running = False
        st.session_state.monitoring_running = False

    if bottom_right.button(
                        "docker check",
                        width="stretch",
                        key="docker_check"
                    ):

        cmd = ["docker", "ps", "-a"]

        status.update(label="Checking status of contaner, volumes, network,...", state="running")
        exit_code = live_command_demo(cmd, log_docker, mode=file_mode)

        if exit_code == 0:
            status.update(
                label="Docker status check completed.", 
                state="complete",
                expanded=False
                )
        else:
            status.update(
                label=f"Checking docker status failed (exit code {exit_code}).", 
                state="error",
                expanded=True,
                )

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