import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Project Status (2)")
    st.markdown("""
    #### (2) APIs
    
    **FastAPI**   
    - Lightweight HTTP interface   
    - Triggers ETL or processing pipelines   
    - Decouples UI from orchestration
    """)
     
    ## 
    # col1, col2, col3 = st.columns(3, border=True)

    # Bsp.-Dateien für Testzwecke
    img = Path("/workspaces/oct25_bmlops_int_rakuten/static files/resnet.png")
    code = Path("src/test.py").read_text(encoding="utf-8")

    with st.expander("trigger 'etl-pipeline'"):
        
        with st.expander("Code"):
            st.code(code, language="python")
        
        st.divider()
       
        if st.button("trigger API call", key="etl"):
            st.write("add LINK to Airflow")
        else:
            st.write("")
       
        # st.divider()

        # st.markdown("""
        # scheduled execution  --> 🟢 every 30d
        # triggered by         --> 🟢 FileSensor + API call
        # """)
    
    with st.expander("trigger 'create similarity matrtix'"):
    
        with st.expander("Code"):
            st.code(code, language="python")
        
        st.divider()
       
        if st.button("trigger API call", key="SimMatrix"):
            st.write("add LINK to Airflow")
        else:
            st.write()
    
    # with col3:
    #     st.markdown("""
    #     ### Make recommendations 
    #     """)
        
    #     st.divider()
        
    #     # with st.popover("Graph"):
    #     #     st.image()
        
    #     st.divider()
       
    #     with st.popover("DAG"):
    #         st.code(code, language="python")
       
    #     st.divider()

    #     st.markdown("""
    #     scheduled execution  --> 🟢 every 30d
    #     triggered by         --> 🟢 FileSensor + API call
    #     """)