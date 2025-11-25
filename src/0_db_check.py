# imports
from utils.setup_helper import setup_mongodb


def main():
    # check MongoDB
    print("Start checking MongoDB")
    try:
        setup_mongodb(verbose=True)
        print("MongoDB check successful.")

    except Exception as e:
        print(f"No MongoDB found.\n{e}")

if __name__ == "__main__":
    main()


