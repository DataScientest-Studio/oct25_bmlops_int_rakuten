ROOT := $(CURDIR)
# ENV ?= core 
# N_NEIGHBORS ?= 5
# MSG ?= auto

.PHONY: setup_environment etl create_embeds

setup_env:
	bash ${ROOT}/src/0_init_setup.sh

repo_push:
	bash ${ROOT}/src/0_repo_push.sh 

etl:
	bash ${ROOT}/src/1_ETL.sh

# create_embeds:
# 	bash ${ROOT}/src/2_create_embeds.sh 

data_split:
	bash ${ROOT}/src/3_data_split.sh

# create_sim_mat:
# 	bash ${ROOT}/src/3_create_SimMat.sh ${ENV} ${N_NEIGHBORS}

# recommend:
# 	bash ${ROOT}/src/4_recommend.sh ${ENV} ${N_NEIGHBORS}

