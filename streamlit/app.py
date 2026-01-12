import streamlit as st
import sys
from pathlib import Path

from pages import (pres_0_home, pres_1_intro , pres_2_pipelines, pres_3_apis,
                    pres_4_mlflow, pres_5_docker, pres_6_monitoring, 
                    pres_7_conclusion) # , pres_8_take_home_msg, pres_3_study_design,  #, results_exemple_train, results_exemple_test                   # pages for 'extras'

# configuration
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

# === Section 1: Project Presentation ===
st.sidebar.markdown("#### 🎥 Project Presentation")        # .expander
presentation = st.sidebar.radio(
    "Chapter:",
    options=[
        "🏠 Home",
        "🧭 Introduction",
        "🛠️ Pipelines & Airflow",
        "🔌 APIs",
        "🧪 MLflow",
        "📦 Docker",
        "📡 Monitoring",
        "🏁 Conclusion",
        # " Take home message"
        # 
        # 
        # " Take home message"
            ],
    key="presentation",              # persist selection across reruns
    index=0,
    # on_change=clear_others,
    args=("presentation",)
    )


PAGES_PRESENTATION = {
    "🏠 Home": pres_0_home.show,
    "🧭 Introduction": pres_1_intro.show,
    "🛠️ Pipeline & Airflow": pres_2_pipelines.show,
    "🔌 APIs": pres_3_apis.show,
    "🧪 MLflow": pres_4_mlflow.show,
    "📦 Docker": pres_5_docker.show,
    "📡 Monitoring": pres_6_monitoring.show,
    "🏁 Conclusion": pres_7_conclusion.show
            }

PAGES_PRESENTATION[presentation]()


# Choose a X-ray",
#         # "🎯 Run Prediction",
#         # " Grad-CAM Visualization",
#         # "🔍

# # from app.utils import c
# from app.utils.loader import load_model, load_image
# from app.utils.predict import predict_image
# from partials.header import render_header
# from app.partials.sidebar import render_sidebar
# from pages import demo_1_upload_select, demo_2_prediction, demo_3_gradcam, pres_5_results_dataviz      # pages for 'presentation'
# from pages import demo_4_shap                      # pages for 'demo'
# from pages import extra_intro
# 
# === Section 2: Prediction ===
# with st.sidebar.expander("### ⚡ Live Demo (Prediction)"):
#     demo = st.radio(
#     "Select topic:",
#     # options=
#     [

    # " Take home message": pres_8_take_home_msg.show
    # "🧠 Results (Training)": results_exemple_train.show,
    # "📈 Results (Table)": pres_4_results_table.show,
    # "📊 Results (DataViz)": pres_5_results_dataviz.show,
    # " Take home message": pres_6_take_home_msg.show
    # "📈 Results": pres_results.show,
    # "Conclusion": ??.show,
    # "Prospects": ??.show
    # "Credits": ??.show
#         # "🖼️ Choose a X-ray",
#         # "🎯 Run Prediction",
#         # "🌈 Grad-CAM Visualization",
#         # "🔍 SHAP Explanation",             
#        # " Prediction",
#        # "Credits",
#     ],
#     key="demo",
#     index=None,
#     on_change=clear_others,
#     args=("demo",)
#     )


# # === Section 3: Additional Results ===
# with st.sidebar.expander("### 📚 Additional Results"):
#     extra = st.radio(
#     "Select analysis:",
#     # options=
#     [
#             # "Model Performance",
#             # "Confusion Matrices",
#         ],
#     key="extra",
#     index=None,
#     on_change=clear_others,
#     args=("extra",)
#         )

# PAGES_DEMO = {
# #             "🖼️ Choose a X-ray": demo_1_upload_select.show,
# #             "🎯 Run Prediction": demo_2_prediction.show,
# #             "🌈 Grad-CAM Visualization": demo_3_gradcam.show,
# #             "🔍 SHAP Explanation": demo_4_shap.show
# #             "Run Prediction": prediction.show,
# #     "Grad-CAM Visualization": gradcam.show,
# #     "SHAP Explanation": shap.show,
#                 }

# PAGES_EXTRA = {
# #         "Intro": extra_intro.show
#     #     "🧠 Results (Training)": results_exemple_train.show,
#     #    "📈 Results (Testing)": results_exemple_test.show, 
# #   "Confusion Matrices": conf_matrices.show,
# #     "Classification Reports": class_reports.show,
# #     "Model Comparison": model_comparison.show,
# #     "Credits": credits.show,
#                     }

# selected = [presentation, demo, extra]
# non_empty = [s for s in selected if s] 

# if len(non_empty) > 1:
#     st.warning("⚠️ **Please, select only one page at a time.**")
#     # selection = presentation or demo or extra

# elif len(non_empty) == 0:
#     st.info("ℹ️ **Please select a page to display.**")

# else:
#     if presentation in PAGES_PRESENTATION:
#         PAGES_PRESENTATION[presentation]()
    
#     elif demo in PAGES_DEMO:
#         PAGES_DEMO[demo]()
    
#     elif extra in PAGES_EXTRA:
#         PAGES_EXTRA[extra]()
