ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PROJECT := rakuten

.PHONY: setup_env repo_push mlflow etl all_docker stop_docker streamlit #  etl create_embeds evaluation fire-alert reports  


setup_env:
	${ROOT}/scripts/0_init_setup.sh

mlflow_local:
	${ROOT}/scripts/0_setup_mlflow.sh 

# docker_all: 
# 	docker compose -p $(PROJECT) --env-file env-f $(ROOT)/docker-compose.yaml up --build -d

# docker_stop:
# 	???

airflow_docker:
	docker compose -p $(PROJECT) --env-file env/airflow.env -f $(ROOT)/docker-compose.airflow.yaml up --build -d

airflow_stop:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.airflow.yaml down

api_docker:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.api.yaml up --build -d

api_stop:
	docker compose -p $(PROJECT)  -f $(ROOT)/docker-compose.api.yaml down

monitoring_docker:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.monitoring.yaml up --build -d

monitoring_stop:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.monitoring.yaml down

streamlit:
	streamlit run $(ROOT)/streamlit/app.py --server.port=8501 --server.address=0.0.0.0
# -------------------------------------------------------------------------

# ROOT := $(CURDIR)
# ENV ?= core 
# N_NEIGHBORS ?= 5
# MSG ?= auto
# MODE == 
# NUM ==

# stop_all_docker: 
# 	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.yaml down

# repo_push:
# 	bash "${ROOT}/scripts/0_repo_push.sh" 

# etl:
# 	bash "${ROOT}/scripts/1_ETL.sh"


# evaluation:
# 	docker compose -p $(PROJECT)-f $(ROOT)/docker-compose.eval.yaml up --build -d

# fire-alert:
# 	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.yaml stop bike-api

# reports:
# 	python3 $(ROOT)/src/main_drift.py


# create_embeds:
# 	bash ${ROOT}/scripts/2_create_embeds.sh 

# data_split:
# 	bash ${ROOT}/scripts/0_data_split.sh ${MODE}=split ${NUM}

# sample_data:
# 	bash ${ROOT}/scripts/0_sample_data.sh ${MODE}=split ${NUM}

# create_sim_mat:
# 	bash ${ROOT}/src/3_create_SimMat.sh ${ENV} ${N_NEIGHBORS}

# recommend:
# 	bash ${ROOT}/src/4_recommend.sh ${ENV} ${N_NEIGHBORS}



