ROOT := $(CURDIR)
ENV_MODE ?= local 
N_NEIGHBORS ?= 5
MSG ?= auto

.PHONY: setup_environment etl create_embeds

setup_env:
	bash ${ROOT}/src/0_init_setup.sh ${ENV_MODE}

repo_push:
	bash ${ROOT}/src/0_repo_push.sh ${MSG}

etl:
	bash ${ROOT}/src/1_ETL.sh ${ENV_MODE}

create_embeds:
	bash ${ROOT}/src/2_create_embeds.sh 

create_sim_mat:
	bash ${ROOT}/src/3_create_SimMat.sh ${ENV_MODE} ${N_NEIGHBORS}

recommend:
	bash ${ROOT}/src/4_recommend.sh ${ENV_MODE} ${N_NEIGHBORS}

