import streamlit as st

def show():
    st.header("📑 Project Status (2)")
    st.markdown("""(2) APIs""")
     
    ## 
    col1, col2, col3 = st.columns(3, border=True)

    with col1:
        st.markdown("""
        ### trigger 'etl-pipeline' 
        """)
        
        st.dividerr()
        
        with st.expander("Code"):
            st.code()
        
        st.dividerr()
       
        if st.button("trigger API call"):
            st.write("add LINK to Airflow")
        else:
            st.write("")
       
        # st.dividerr()

        # st.markdown("""
        # scheduled execution  --> 🟢 every 30d
        # triggered by         --> 🟢 FileSensor + API call
        # """)
    
    with col2:
        st.markdown("""
        ### trigger 'create simmilarity matrtix'
        """)
        
        st.dividerr()

        with st.expander("Code"):
            st.code()
        
        st.dividerr()
       
        if st.button("trigger API call"):
            st.write("add LINK to Airflow")
        else:
            st.write()
    
    with col3:
        st.markdown("""
        ### Make recommendations 
        """)
        
        st.divider()
        
        with st.popover("Graph"):
            st.image()
        
        st.divider()
       
        with st.popover("DAG"):
            st.code()
       
        st.divider()

        st.markdown("""
        scheduled execution  --> 🟢 every 30d
        triggered by         --> 🟢 FileSensor + API call
        """)