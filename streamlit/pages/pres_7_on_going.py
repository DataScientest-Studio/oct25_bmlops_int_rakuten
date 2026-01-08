import streamlit as st
from pathlib import Path

def show():
    st.header("📑 Project Status (6)")
    st.markdown("""
    #### (5) On-going approaches
  
    **GitHub Actions**   
    - Automated CI/CD pipelines triggered by repository events   
    - Execution of tests, linters, and build steps on code changes   
    - Enforcement of code quality and reproducibility across environments

    **Terraform (incl. Amazon Machine Image (AMI))**
    - Infrastructure-as-Code (IaC) for declarative cloud resource provisioning   
    - Definition and versioning of compute, networking, and storage resources   
    - Use of AMIs to ensure reproducible VM environments

    """)