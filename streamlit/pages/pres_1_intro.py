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

        

        st.subheader("The data")
        st.markdown('''
        - Rakuten Product Dataset
        - Consists of approximately 99.000 product listings (85k train and 14k test)
        - For each product, the following information where given (CSV):
            - productid - unique identifier
            - designation - short description
            - describtion - long description (sometimes missing)
            - imageid - unique identifier for images
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
        - Orchestration of Pipelines (ETL, 'training') (**Airflow**)
        - API Deployment (**FastAPI**)
        - Experiment tracking (**MLflow**)
        - Containerisation / Microservice architecture (**Docker**)
        - Monitoring & Maintenance (**Prometheus**, **Grafana**, **Node-explorer**) 
        - On-going
        """)
