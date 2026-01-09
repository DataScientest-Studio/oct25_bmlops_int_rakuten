import numpy as np
import pickle
from pathlib import Path
from utils.setup_helper import get_latest_training_folder, load_env_vars
from utils.settings import session


class KNNService:
    def __init__(self, n_neighbors=10):
        load_env_vars()

        if session.root is None:
            session.root = Path(".").resolve()
        if session.data is None:
            session.data = session.root / "data"

        MODEL = session.data / "models"
        latest_dir = get_latest_training_folder(MODEL).name
        self.SM_FOLDER = MODEL / latest_dir

        # -------- Load data once --------
        with open(self.SM_FOLDER / "idx_map.pkl", "rb") as f:
            self.id_to_index = pickle.load(f)

        self.product_ids = np.load(self.SM_FOLDER / "knn_product_ids.npy")
        self.topk_neighbors = np.load(
            self.SM_FOLDER / f"knn_top{n_neighbors}_neighbors.npy"
        )

    def get_recommendations(self, productid: int):
        if productid not in self.id_to_index:
            return None

        idx = self.id_to_index[productid]
        neighbors = self.topk_neighbors[idx]
        return self.product_ids[neighbors].tolist()
