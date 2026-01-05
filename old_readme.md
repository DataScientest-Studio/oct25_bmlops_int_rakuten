# 🦠 COVID-19 Chest X-ray Classification Project

This project includes notebooks, scripts and a streamlit application on 'multi-class classification of chest x-ray images'. The goal of the project is to reliably classify chest x-ray images (covid-19, normal, lung opacity, and viral pneumonia) and gain further insight into how the convolutional neuronal network applied (ResNet 50) make its predictions.   
The following dataset from kaggle was used in scope of training the model: [Original dataset](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database) 

## Project Structure

```text
|- notebooks                     <- Reports (Jupyter notebooks) on EDA, CNN training and model evaluation.
|   |- helper                    <- Includes py-files containing the necessary functions for conducting studies 
                                    covered in 'notebooks' 
|- report                        <- Contains a summarizing report on the entire study
|- streamlit                     <- Includes necessary files for executing streamlit application.
|   |- streamlit_app.py
|   |- requirements.txt
|   |- app                       <- Contains the streamlit application and its pages.
|   |   |- pages                 <- Contains pages of streamlit app
|   |   |- static files          <- Contains raw and processed data 
|   |   |   |- ClassReport       <- Contains Classification Reports for all training stages
|   |   |   |- ConfMatrix        <- Contains Confusion Matrices for all training stages
|   |   |   |- GradCam           <- Contains GradCAM images for all training stages
|   |   |   |- SHAP              <- Contains SHAP images for all training stages
|   |   |   |- best_hp_df        <- Contains tables of in-run metrics and applied hyperparamater setting for all
                                    trials in all training stages
|   |   |   |- eda_files         <- Contains excel files on metadata of dataset used
|   |   |   |- prediction_df     <- Contains tables on prediction results (incl. probabilities) for all training
                                    stages
|   |   |   |- sparsity_scores   <- Contains tables on sparsity scores of GradCAM and SHAP images for all
                                    training stages  
|   |   |- utils                 <- Includes py-files containing the necessary functions for executing the
                                    streamlit app
|   |- models                    <- Contains weight.file of the final ResNet 50 model (used for demo part)
|   |- venv_app                  <- Contains files of the virtual environment

```

--------

## Project Information

This project is described in a report (`~/reports/report_RF`) summarizing the single training reports (`~/notebooks`). For a better understanding, the streamlit application on the project should also be taken into account (`~/streamlit`).

## Setup Guide (streamlit app)

1. Activate venv (for Linux and macOS)
   ```bash
   source ~/streamlit/venv_app/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip install -r ~/streamlit/requirements.txt
   ```
3. Run the streamlit application:
   ```bash
   streamlit run ~/streamlit/streamlit_app.py
   ```
5. Open your browser and navigate to `http://localhost:8501` to view the application.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
