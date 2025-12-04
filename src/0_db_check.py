## 0_db_check.py
# imports
import src.utils.database_helper as dbh
# import utils.setup_helper as sh # import setup_mongodb


def main():
    # check MongoDB
    print("Start checking MongoDB")
    try:
        dbh.setup_mongodb(verbose=True)
        print("MongoDB check successful.")

    except Exception as e:
        print(f"No MongoDB found.\n{e}")

if __name__ == "__main__":
    main()


