ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PROJECT := rakuten

.PHONY: setup_env mlflow_local traffic all_stop all_remove airflow_docker airflow_stop api_docker api_stop ml_stop ml_docker streamlit monitoring_docker monitoring_stop


setup_env:
	${ROOT}/scripts/0_init_setup.sh

mlflow_local:
	${ROOT}/scripts/0_setup_mlflow.sh 

traffic:
	python3 streamlit/src/generate_traffic.py

all_stop:
	@docker ps -aq | xargs -r docker stop

all_remove:
	@docker ps -aq | xargs -r docker rm -v

airflow_docker:
	docker compose -p $(PROJECT) --env-file env/airflow.env -f $(ROOT)/docker-compose.airflow.yaml up --build -d

airflow_stop:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.airflow.yaml down

api_docker:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.api.yaml up --build -d

api_stop:
	docker compose -p $(PROJECT)  -f $(ROOT)/docker-compose.api.yaml down

ml_docker:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.ml.yaml up --build -d

ml_stop:
	docker compose -p $(PROJECT)  -f $(ROOT)/docker-compose.api.yaml down
	
monitoring_docker:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.monitoring.yaml up --build -d

monitoring_stop:
	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.monitoring.yaml down

streamlit:
	streamlit run $(ROOT)/streamlit/app.py --server.port=8501 --server.address=0.0.0.0
