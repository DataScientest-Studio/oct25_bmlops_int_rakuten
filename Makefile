ROOT := $(CURDIR)
ENV_MODE ?= local 
N_NEIGHBORS ?= 5

.PHONY: setup_environment etl create_embeds

setup environment:
	bash ${ROOT}/src/0_init_setup.sh ${ENV_MODE}

etl:
	bash ${ROOT}/src/1_ETL.sh ${ENV_MODE}

create embeds:
	bash ${ROOT}/src/2_create_embeds.sh 

create sim_mat:
	bash ${ROOT}/src/3_create_SimMat.sh ${ENV_MODE} ${N_NEIGHBORS}

recommend:
	bash ${ROOT}/src/4_recommend.sh ${ENV_MODE} ${N_NEIGHBORS}

