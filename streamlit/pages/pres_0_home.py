import streamlit as st

def show():
    # st.header("🏠 Home")
    st.set_page_config(page_title="Rakuten e-commerce recommendation system", layout="wide")
    
    st.subheader("🏠 MLOps project 'Rakuten recommendation app'")
    path_img_infra = "/workspaces/oct25_bmlops_int_rakuten/streamlit/static_files/Infra_overview_2.png"
    st.image(path_img_infra,
            caption="Overview infrastructure, made with Mermaid",
            width=1000)
    
