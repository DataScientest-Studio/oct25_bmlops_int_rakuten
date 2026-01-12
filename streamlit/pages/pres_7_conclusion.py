import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Conclusion")
    st.markdown("""
    #### What is the Status Quo of our project?
    """)
    with st.expander("**(1) Automated processes**"):
        st.markdown("""
        ✅ Pipelines and orchestration are available   
        ✅ Can be triggered by API   
        🟡 Adding a FileSensor or similar (--> increase automation)
        """)
        
    with st.expander("**(2) User interactions possible**"):
        st.markdown("""
        ✅ API endpoints 'etl_trigger', 'create SimMatrix' and 'recommendation' available   
        🔴 Basic Auth or OAuth2 no yet implemented
        """)
        

    with st.expander("**(3) File and Data storage**"):
        st.markdown("""
        ✅ Product data: MongoDB   
        ✅ Airflow: PostgreSQL
        🔜 MLflow: SQLite or PotsgreSQL possible   
        🔜 use additional and more specialised/optimised DBs (e.g. SQL, vector DB)
        """)
        

    with st.expander("**(4) 'Best' Model available and ensured**"):
        st.markdown("""
        ✅ Suitable model at hand
        ✅ Tracked its building (**MLflow**)   
        🟡 Model selection: also tried FAISS but not completed (*Facebook AI Similarity Search*)   
        🔴 Model optimisation: try **Optuna**
        🔴 Selection and optimisation not semi-automated   
        🔴 Adding further data on 'products' (unlabelled Rakuten set, AI generated) then agreement-filtered pseudo-labelling   
        🔴 Adding AI generated data on 'customers', 'baskets' and/or 'orders'   
        --> creating an hybrid-approach recommendation system
        """)
       
    with st.expander("**(5) Monitoring & Maintenance**"):
        st.markdown("""
        ✅ Prometheus, Node-exporter and Grafana are available and interconnected
        🟡 Loki: available but not yet fully configured and integrated
        🔴 centralised logging to faciliate debugging and troubleshooting    
        🔴 connect to other tools, e.g. MLflow, Airflow 
        """)


    with st.expander("**(6) Reliability**"):
        st.markdown("""
        - ci.yaml and milestone.yaml   
        ✅ both: creation started   
        ✅ ci: sucessfully triggered by 'pull_request'   
        🟡 milestone: supposed to be triggered by change in tag 'version' (subversion: v1.1 --> v1.2)   
        🟡 Debug status: not yet ready and unclear, respectively   
        🟡 Unit Tests: more to be added   
        🔴 pre-commit hooks: not yet started (i.e. black, flake8,..)
        - release   
        🔴 not yet started   
        🔴 supposed to be triggered by change in tag 'version' (version: v1.* --> v2.0)
    """)


    with st.expander("**(7) Availability, Portability and Scalability**"):
        st.markdown("""   
        - Docker   
        ✅ all tools dockerized so far   
        ✅ Compose and decompose w/o errors    
        ✅ Makefile: semi-automated processes and SAME network ensured   
        ✅ Docker-compose + Dockerfile: ensures portability and scalability   
        🔜 Better overview: use 'Portainer'or 'ContainerTools' (= VSCode extension)
        - Kubernetes   
        🔴 not yet started   
        - Terraform (i.e. IaC wrt EC2, subnets, security groups, routing tables, NAT-/IGW,...)   
        🔴 not yet started
        - Amazon Machine Image (AMI):   
        🟡 MLOps base image available, additional AMIs possible as backup or when production ready (--> autoscaling)   
        - Grafana   
        ✅ dashboards: DataViz and Monitoring as IaC
    """)

    with st.popover("ℹ️ AMI 'MLOps base'"):
        st.write("")

# - Product Classification and Clustering
#         - Testing other models and 'Model' optimization (**Optuna**)
#         - 
#         -   
        
#      ();  BUT not fully debugged (see error reports)   
#     : creation started, 'pull_request' BUT not fully debugged (see error reports)  
#     started creating milestone.yaml (--> triggered by 'pull_request') but not fully debugged (see error reports by e-mail)  
    
    
    
#     --> CI/CD pipelines and Unit testing  


#      --> Model selection and experiment tracking   
#          --> wrt infrastructure, application and model   
         
#          --> quick adaption to short-/long-term changes and fluctuations 


#          --> Pipelines + orchestration  
#          --> API deployment + security   
#          --> Databases   
        
#         On-going 
#         - API security (BasicAuth or OAuth2)
#         - CI/CD pipelines (**GitHub Actions**)
#         - Unit Testing
#         - Portability (**AMI**, **Terraform**)


#         (Almost) completely covered 
#         - Pipelines (ETL, 'training', recommendation)
#         - Orchestration (**Airflow**)
#         - API Deployment (**FastAPI**)
#         - Store data in databases (**SQLite**, **MongoDB**)
#         - Experiment tracking (**MLflow**)
#         - Containerisation / Microservice architecture (**Docker**)
#         - Monitoring & Maintenance (**Prometheus**, **Grafana**, **Node-explorer**) 

#         Not yet started and future plans
#         - Scalability (**Kubernetes**)
        