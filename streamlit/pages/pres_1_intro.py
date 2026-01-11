import streamlit as st

def show():
    st.header("🏠 Introduction")
    st.write("What is the need for a recommendation app?") 

    # st.write("{text from report}")

    tabs = st.tabs(["Context", "Table of contents"])

    # :material/subdirectory_arrow_right

    with tabs[0]:     
        st.subheader("The data")
        st.markdown('''
        - Rakuten Product Dataset
        - Consists of approximately 99.000 product listings (85k train and 14k test)
        - For each product, the following information where given (CSV):
            - productid - unique identifier
            - designation - short description
            - describtion - long description (sometimes missing)
            - imageid - unique identifier for images
            - prdtypecode - represents the product category (only available for train data)
        - Additionally, a ZIP-File containing images for every product was given
        ''')
        
        st.subheader("The model")
        st.markdown('''
        - Recommender system
        - Create embeddings for image and text data and combine them -> no training in classical sense
        - Recommendation based on the embeddings with the closest distance
        - Evaluation of the model based on how many of the 10 best recommendations (for each product) have the same prdtypecode -> only use train data
        ''')

    with tabs[1]:
        st.subheader("Table of Contents")
        st.markdown("""
        **What is necessary to have a production ready application?**
        
        **(1) Automated processes** --> Pipelines + orchestration  
        **(2) User interactions possible** --> API deployment + security   
        **(3) File and Data storage** --> Databases   
        **(4) 'Best' Model available and ensured** --> Model selection and experiment tracking   
        **(5) Monitoring & Maintenance** --> wrt infrastructure, application and model   
        **(6) Reliability** --> CI/CD pipelines and Unit testing   
        **(7) Portability and Scalability** --> quick adaption to short-/long-term changes and fluctuations 

        - Orchestration of Pipelines (ETL, 'training') (**Airflow**)
        - API Deployment (**FastAPI**)
        - Experiment tracking (**MLflow**)
        - Containerisation / Microservice architecture (**Docker**)
        - Monitoring & Maintenance (**Prometheus**, **Grafana**, **Node-explorer**) 
        - On-going
        """)
