## 0_data_split.py
# imports
import pandas as pd
import click
# import importlib

import utils.setup_helper as sh
import utils.db_helper as dh
from utils.data_handling import list_products, create_subgroups

# importlib.reload(dh)


# ---------
# 
# ------------

@sh.cli_or_api
def main(fname, num):
    # configuration
    coll_name = "products"
    cols_needed = None 

    # loading data from 
    if not fname:
        df = dh.load_cursor(coll_name, cols_needed)
    
    else:
        from pathlib import Path
        from utils.settings import session

        sh.load_env_vars()
        sh.get_paths()

        DATA = session.data
        DATA_LAKE = DATA / "data_lake"
        file_path = DATA_LAKE / Path(fname)
        df = pd.read_csv(file_path) # pd.read_csv("")

    if df is None:
        print(" Error - creating data from file or database.")
        return None

    product_ids = list_products(df)
    
    if num:
        create_subgroups(product_ids, num, coll_name)
    

@click.command()
@click.option("--fname",
              type=str,
              default=None,
              required=False)
@click.option("--num",
              type=int,
              required=False)
def main_entry_check(fname, num):
    main(fname, num)

if __name__ == "__main__":
    main_entry_check()

   