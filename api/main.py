from fastapi import FastAPI, HTTPException
from .knn_service import KNNService
from .etl_trigger import router as etl_router
from .train_trigger import router as train_router

app = FastAPI(title="KNN Recommendation API")

knn = KNNService(n_neighbors=10)
app.include_router(etl_router)
app.include_router(train_router)

@app.get("/health")
def health():
    return {"status": "ok"}



#@app.get("/recommend/{product_id}")
@app.get("/recommend/{productid}")
def recommend(productid: int):
    recs = knn.get_recommendations(productid)

    if recs is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product {productid} not found"
        )

    return {
        "productid": productid,
        "recommendations": recs
    }
