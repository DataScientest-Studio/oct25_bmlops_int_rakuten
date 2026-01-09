# similarity_helper.py
# imports
#import faiss
import gridfs
import numpy as np

from sklearn.neighbors import NearestNeighbors

import utils.db_helper as dh

def parse_embedding(s: str):
    return np.array(s.split(","), dtype=np.float32)

def create_array(docs, normalize=None):
    # create numpy arrays for recommender system
    product_ids = np.array([d["productid"] for d in docs], dtype=np.int64)
    text_emb = np.array([d["text_embed"] for d in docs], dtype=np.float32)
    #image_emb= np.array([d["embedding_str"] for d in docs], dtype=np.float32)
    image_emb = np.array([parse_embedding(d["embedding_img"]) for d in docs], dtype=np.float32)
    # create id to index mapping
    id_to_index = {pid: i for i, pid in enumerate(product_ids)}

    # if necessary, normalize vectors
    # if normalize:
    #     if normalize == True:
    #         image_emb = l2_norm(image_emb) 
    #         txt_emb = l2_norm(text_emb)

    #     if isinstance(normalize, dict):
    #         if normalize["image"] == True:
    #             image_emb = l2_norm(image_emb)

    #         if normalize["text"] == True:
    #             text_emb = l2_norm(text_emb)
    return product_ids, text_emb, image_emb, id_to_index
                      
def combine_txt_img(image_emb, text_emb, alpha):
    # combining vectors to recommender system matrix
             # weight for image vector
    beta = 1- alpha      # weight for text vector

    embed_comb = np.hstack([alpha * image_emb, beta * text_emb])
    embed_comb = l2_norm(embed_comb.astype("float32"))

    return embed_comb


def create_knn_sm(array, metric="cosine", num_k=5):
    knn = NearestNeighbors(metric=metric, 
                       n_neighbors=num_k)
    knn.fit(array)
    arr_top_k = knn.kneighbors(array, return_distance=False)
    return arr_top_k
    

#def create_faiss_idx(array, path):
#    if array.dtype != np.float32:
#        array = array.astype(np.float32)

#    d = array.shape[1]
#    index = faiss.IndexFlatIP(d)  # Using Inner Product for Cosine Similarity
#    index.add(array) 

    # save index locally
#    faiss.write_index(index, str(path))
#    print("FAISS index locally saved.")
#    return index

#def save_faiss_to_mongo(path: str, db_name: str=None):
#    db, _, _, = dh.setup_mongodb(db_name=db_name)
#    fs = gridfs.GridFS(db)

#    f_path = path / "faiss_index.bin"
#    with open(f_path, "rb") as f:
#        file_id = fs.put(f, filename="faiss_index")
#        print("FAISS index loaded to MongoDB.")
#        return file_id

#def load_faiss_from_mongo(db_name, filename="faiss_index"):
#    db, _, _, _ = dh.setup_mongodb(db_name=db_name)
#    fs = gridfs.GridFS(db)

#    file_data = fs.find_one({"filename": filename})
#    if not file_data:
#        raise ValueError("FAISS index not found in MongoDB.")

#    bin_data = file_data.read()

    # Temporäre Datei erzeugen
#    import tempfile
#    with tempfile.NamedTemporaryFile(delete=False) as tmp:
#        tmp.write(bin_data)
#        tmp_path = tmp.name

#    return faiss.read_index(tmp_path)

#def faiss_search(index: faiss.Index, query: np.ndarray, k=10):
#    if query.dtype != np.float32:
#        query = query.astype(np.float32)

#    D, I = index.search(query, k)  
    # D = distances, shape (1, k)
    # I = indices    shape (1, k)

#    return I[0], D[0]

def l2_norm(x):
        return x / np.linalg.norm(x, axis=1, keepdims=True)

