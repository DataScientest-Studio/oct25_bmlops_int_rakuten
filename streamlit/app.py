import streamlit as st
# from app.utils import c
# from app.utils.loader import load_model, load_image
# from app.utils.predict import predict_image
# from partials.header import render_header
# from app.partials.sidebar import render_sidebar
# from pages import demo_1_upload_select, demo_2_prediction, demo_3_gradcam, pres_5_results_dataviz      # pages for 'presentation'
# from pages import demo_4_shap                      # pages for 'demo'
# from pages import extra_intro
from pages import pres_0_home, pres_1_intro #, pres_2_approach_eda, pres_3_study_design, pres_4_results_table, pres_5_results_dataviz, pres_6_take_home_msg #, results_exemple_train, results_exemple_test                   # pages for 'extras'

                    
def clear_others(active_key):
    for key in ["presentation", "demo", "extra"]:
        if key != active_key and key in st.session_state:
            st.session_state[key] = None


# === Section 1: Project Presentation ===
with st.sidebar.expander("#### 🎥 Project Presentation"):
    presentation = st.radio(
    "Chapter:",
    # options=
    [   "🏠 Home",
        "📑 Introduction",
        "🩺 Approach and EDA",
        "📑 Study design",
        # "🧠 Results (Training)",
        "📈 Results (Table)",
        "📊 Results (DataViz)",
        " Take home message"
            ],
    key="presentation",              # persist selection across reruns
    index=None,
    on_change=clear_others,
    args=("presentation",)
    )

# === Section 2: Prediction ===
with st.sidebar.expander("### ⚡ Live Demo (Prediction)"):
    demo = st.radio(
    "Select topic:",
    # options=
    [
        "🖼️ Choose a X-ray",
        "🎯 Run Prediction",
        "🌈 Grad-CAM Visualization",
        "🔍 SHAP Explanation",             
       # " Prediction",
       # "Credits",
    ],
    key="demo",
    index=None,
    on_change=clear_others,
    args=("demo",)
    )


# === Section 3: Additional Results ===
with st.sidebar.expander("### 📚 Additional Results"):
    extra = st.radio(
    "Select analysis:",
    # options=
    [
            "Model Performance",
            "Confusion Matrices",
        ],
    key="extra",
    index=None,
    on_change=clear_others,
    args=("extra",)
        )

PAGES_PRESENTATION = {
    "🏠 Home": pres_0_home.show,
    "📑 Introduction": pres_1_intro.show,
    "🩺 Approach and EDA": pres_2_approach_eda.show,
    "📑 Study design": pres_3_study_design.show,
    # "🧠 Results (Training)": results_exemple_train.show,
    # "📈 Results (Table)": pres_4_results_table.show,
    # "📊 Results (DataViz)": pres_5_results_dataviz.show,
    # " Take home message": pres_6_take_home_msg.show
    # "📈 Results": pres_results.show,
    # "Conclusion": ??.show,
    # "Prospects": ??.show
    # "Credits": ??.show
            }

# PAGES_DEMO = {
#             "🖼️ Choose a X-ray": demo_1_upload_select.show,
#             "🎯 Run Prediction": demo_2_prediction.show,
#             "🌈 Grad-CAM Visualization": demo_3_gradcam.show,
#             "🔍 SHAP Explanation": demo_4_shap.show
#             "Run Prediction": prediction.show,
#     "Grad-CAM Visualization": gradcam.show,
#     "SHAP Explanation": shap.show,
                # }

# PAGES_EXTRA = {
#         "Intro": extra_intro.show
    #     "🧠 Results (Training)": results_exemple_train.show,
    #    "📈 Results (Testing)": results_exemple_test.show, 
#   "Confusion Matrices": conf_matrices.show,
#     "Classification Reports": class_reports.show,
#     "Model Comparison": model_comparison.show,
#     "Credits": credits.show,
                    # }

selected = [presentation, demo, extra]
non_empty = [s for s in selected if s] 

if len(non_empty) > 1:
    st.warning("⚠️ **Please, select only one page at a time.**")
    # selection = presentation or demo or extra

elif len(non_empty) == 0:
    st.info("ℹ️ **Please select a page to display.**")

else:
    if presentation in PAGES_PRESENTATION:
        PAGES_PRESENTATION[presentation]()
    
    elif demo in PAGES_DEMO:
        PAGES_DEMO[demo]()
    
    elif extra in PAGES_EXTRA:
        PAGES_EXTRA[extra]()
