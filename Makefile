ROOT := $(CURDIR)
# ENV ?= core 
# N_NEIGHBORS ?= 5
# MSG ?= auto
# MODE == 
# NUM ==

.PHONY: setup_env repo_push mlflow etl   # etl create_embeds

setup_env:
	bash "${ROOT}/scripts/0_init_setup.sh"

repo_push:
	bash "${ROOT}/scripts/0_repo_push.sh" 

mlflow:
	bash "${ROOT}/scripts/0_setup_mlflow.sh" 

etl:
	bash "${ROOT}/scripts/1_ETL.sh"

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

# ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
# PROJECT := monitoring

# .PHONY: all stop evaluation fire-alert reports  

# all: 
# 	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.yaml up --build -d

# stop: 
# 	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.yaml down

# evaluation:
# 	docker compose -p $(PROJECT)-f $(ROOT)/docker-compose.eval.yaml up --build -d

# fire-alert:
# 	docker compose -p $(PROJECT) -f $(ROOT)/docker-compose.yaml stop bike-api

# reports:
# 	python3 $(ROOT)/src/main_drift.py

