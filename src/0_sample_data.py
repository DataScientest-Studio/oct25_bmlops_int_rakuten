## 0_sample_data.py
# imports

import click
# import importlib

import utils.setup_helper as sh
import utils.db_helper as dh
from utils.data_handling import list_products, draw_samples

# importlib.reload(dh)


# ---------
# 
# ------------

@sh.cli_or_api
def main(num):
    # configuration
    coll_name = "products"
    cols_needed = None 

    # loading data from 
    df = dh.load_cursor(coll_name, cols_needed)
    
    if df is None:
        print(" Error - creating data from database.")
        return None

    product_ids = list_products(df)
    
    if num:
        draw_samples(product_ids, num, coll_name)
    

@click.command()
@click.option("--num",
              type=int,
              required=False)
def main_entry_check(num):
    main(num)

if __name__ == "__main__":
    main_entry_check()

   