import streamlit as st

def show():
    # st.header("🏠 Home")
    st.set_page_config(page_title="Rakuten e-commerce recommendation system", layout="wide")
    
    st.subheader("🏠 MLOps project 'Rakuten recommendation app'")
    path_img_infra = "/workspaces/oct25_bmlops_int_rakuten/streamlit/static_files/Infra_overview_2.png"
    st.image(path_img_infra,
            caption="Overview infrastructure, made with Mermaid",
            width=1000)
    
    # st.markdown("""
    # #### Multiclass classification of thorax X-ray images by using the convolutional neural network ResNet 50 
    # """)

    # st.image("/workspaces/may25_bds_covid19/streamlit/app/static_files/eda_files/CXR_image.jpg", width=500)
    # st.caption("Von User:Lange123 - User:Lange123, https://de.wikipedia.org/w/index.php?curid=430238")
