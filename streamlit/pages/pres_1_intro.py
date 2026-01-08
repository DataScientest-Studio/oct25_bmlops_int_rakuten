import streamlit as st

def show():
    st.header("🏠 Introduction")
    st.write("What is the need for a recommendation app?") 

    # st.write("{text from report}")

    tabs = st.tabs(["Context", "Scope"])

    # :material/subdirectory_arrow_right

    with tabs[0]:
        st.subheader("Context of the project")
        st.markdown("""
        Cataloging products according to different data (texts and images) is important for e-commerce since it allows for various applications such 
        as product recommendation and personalized research. It is then a question of predicting the type code of the products knowing textual data 
        (designation and description of the products) as well as image data (image of the product).
                        """)

    with tabs[1]:
        st.subheader("Scope of the project")
        st.markdown("""
        (Almost) completely covered 
        - Pipelines (ETL, 'training', recommendation)
        - Orchestration (**Airflow**)
        - API Deployment (**FastAPI**)
        - Store data in databases (**SQLite**, **MongoDB**)
        - Experiment tracking (**MLflow**)
        - Containerisation / Microservice architecture (**Docker**)
        - Monitoring & Maintenance (**Prometheus**, **Grafana**, **Node-explorer**) 
        
        On-going 
        - API security (BasicAuth or OAuth2)
        - CI/CD pipelines (**GitHub Actions*)
        - Unit Testing
        - Portability (**AMI**, **Terraform**)

        Not yet started and future plans
        - Scalability (**Kubernetes**)
        - Product Classification and Clustering
        - Testing other models and 'Model' optimization (**Optuna**)
        - Adding AI generated data on 'products' (incl. agreement-filtered pseudo-labelling)
        - Adding AI generated data on 'customers', 'baskets' and/or 'orders'  
        --> creating an hybrid-approach recommendation system

        """)
