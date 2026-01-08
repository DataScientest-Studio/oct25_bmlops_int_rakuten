import streamlit as st

def show():
    st.header("📑 Project Status (1)")
    st.markdown("(1) Pipelines and orchestration")
     
    ## 
    col1, col2, col3 = st.columns(3, border=True)

    with col1:
        st.markdown("""
        ### ETL (extract - transform - load) 
        """)
        
        st.divider()
        
        with st.popover("Graph"):
            # st.image()
            'hey'

        st.divider()
       
        with st.popover("DAG"):
            st.code()
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 FileSensor + API call
        
        [ADD SHOWCASE MOMENT "FileSensor" 
        + LINK TO AIRFLOW (st.link_button(name, url))]
        """)
    
    with col2:
        st.markdown("""
        ### Create simmilarity matrtix
        """)
        
        st.divider()
        
        with st.popover("Graph"):
            # st.image()
            'hey'
        
        st.divider()
       
        with st.popover("DAG"):
            st.code()
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 FileSensor + API call
        """)
    
    with col3:
        st.markdown("""
        ### Make recommendations 
        """)
        
        st.divider()
        
        with st.popover("Graph"):
            # st.image()
            'hey'
        
        st.divider()
       
        with st.popover("DAG"):
            st.code()
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 FileSensor + API call
        """)