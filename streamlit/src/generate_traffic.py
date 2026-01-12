# import json
import requests
import numpy as np
# import pandas as pd
# import datetime
import io
# import zipfile
import time
import os
import sys
import warnings

# import utils


# configurations
API_URL = "https://bookish-space-train-v6r9vrjvrjj9fwqwp-8001.app.github.dev/french"
N_RUNS = 100 

def generate_traffic(url, count: int):
    """
    Generates simulated traffic to an API endpoint.
    """
    print(f"\n--- Generating {count} requests to {url} ---")

    n_errors = 0
    n_requests = 0

    for i in range(count):

        if n_errors > 10:
            print("\n[ERROR --> EXIT] More than 10 errors occured. Thus, script is stopped now.\n")
            # break 
            sys.exit(2)

        SLEEP_SECONDS = 10*float(np.random.random(
                            size=1, 
                            # random_state=42
                            ))
        if i % 10 == 0:
            print(f"  - Sending request {i+1}/{count}...")
        
        response = requests.get(url)  
                                # json=sample_features_copy, 
                                # timeout=10)

        n_requests += 1

        if response.status_code != 200:
            n_errors += 1
            continue

        print(f"[response.status_code]\t{response.text}")

        

        # response.raise_for_status()
        time.sleep(SLEEP_SECONDS)

        
    print(f"{n_requests} API requests sent.")

if __name__ == "__main__":
    generate_traffic(url=API_URL, count=N_RUNS)

#     predict_sample_df = full_data   # .loc['2011-01-01 00:00:00':'2011-01-31 23:00:00'].copy()
#     if predict_sample_df.empty:
#         print("Warning: No data for prediction traffic. Check date ranges.")
#         return

#     if predict_sample_df.shape[0] < count:
#         print("Warning: Not enough data for prediction traffic. Using available data.")
#         predict_samples = predict_sample_df.to_dict(orient='records')                       # [ALL_MODEL_FEATS + [DTEDAY_COL_NAME]]
#     else:
#         predict_samples = predict_sample_df.sample(n=count, random_state=42).to_dict(orient='records')          # [ALL_MODEL_FEATS + [DTEDAY_COL_NAME]]

    
# if __name__ == "__main__":
#     utils.load_env_vars()
#     split_dict = utils.prepare_data(feat_dict, jan_11, eda=True, f_path=None) #"/app/model")

#     # raw_data = utils.load_df()
#     generate_traffic(1000, split_dict["X"])  # process_data(_fetch_data())





# # feat_dict = {
# #         'target':'cnt',
# #         'prediction':'prediction',
# #         'num_feat':['temp', 
# #                     'atemp', 
# #                     'hum', 
# #                     'windspeed', 
# #                     'mnth', 
# #                     'hr', 
# #                     'weekday'],
# #         'cat_feat':['season', 
# #                     'holiday', 
# #                     'workingday',
# #                     # 'weathersit'
# #                     ]}
# # jan_11 = ['2011-01-01 00:00:00', '2011-01-28 23:00:00']
# # feb_11 = ['2011-01-29 00:00:00', '2011-02-28 23:00:00'] 
# # week_1 = ['2011-01-29 00:00:00', '2011-02-07 23:00:00']
# # week_2 = ['2011-02-07 00:00:00', '2011-02-14 23:00:00'] 
# # week_3 = ['2011-02-15 00:00:00', '2011-02-21 23:00:00']  

# # # DATASET_URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"
# # # API_EVALUATE_URL = "http://bike-api:8080/evaluate"
# # # Nombre d'échantillons à utiliser pour chaque évaluation

# # WEEKLY_PERIODS = {
# #     'week1_february': ('2011-01-29 00:00:00', '2011-02-07 23:00:00'),
# #     'week2_february': ('2011-02-08 00:00:00', '2011-02-14 23:00:00'),
# #     'week3_february': ('2011-02-15 00:00:00', '2011-02-21 23:00:00')
# # }
# # DEFAULT_EVAL_PERIOD = WEEKLY_PERIODS['week1_february']
# # DEFAULT_PERIOD_NAME = 'week1_february'

# # NUM_FEATS = ['temp', 'atemp', 'hum', 'windspeed', 'mnth', 'hr', 'weekday']
# # CAT_FEATS = ['season', 'holiday', 'workingday', 'weathersit']
# # ALL_MODEL_FEATS = NUM_FEATS + CAT_FEATS
# # TARGET = 'cnt'

# # DTEDAY_COL_NAME = 'dteday'
# # COLUMNS_FOR_EVALUATION_PAYLOAD = ALL_MODEL_FEATS + [TARGET, DTEDAY_COL_NAME]

