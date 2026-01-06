# Rakuten e-commerce product classification

Cataloging products according to different data (texts and images) is important for e-commerce since it allows various applications such as product recommendation and personalized search. It is then a question of predicting the type code of the products knowing textual data (designation and description of the products) as well as image data (image of the product).

---

## Data
This project is part of the challenge Rakuten France Multimodal Product Data Classification, the data and their description are publically [available](https://challengedata.ens.fr/challenges/35).  
Text data: ~60 mb  
Image data: ~2.2 gb  
99k data entries with more than 1000 classes.  

---

## Project Organization
--> Update nötig [tree -H "." -L 4 -d -o ~/tree.html]

<p align="left">
    <a href="tree_commented.html">📁 Full project structure (HTML)</a>
</p>

--------

## Project Information
## Prerequisites
+ python 3.11.x
+ Git
+ Python venv

--------

## Setup Guide

1. Activate venv (for Linux and macOS)
   ```bash
   source .venv/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```
4. Run the streamlit application:
   ```bash
   streamlit run src/app/streamlit_app.py
   ```
5. Open your browser and navigate to `http://localhost:8501` to view the application.



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
