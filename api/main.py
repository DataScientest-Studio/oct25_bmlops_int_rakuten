from fastapi import FastAPI, HTTPException

# Internal application services and routers
from .knn_service import KNNService
from .etl_trigger import router as etl_router
from .train_trigger import router as train_router

# Initialize FastAPI app with metadata
app = FastAPI(title="KNN Recommendation API")

# Initialize KNN recommendation service
# n_neighbors defines how many similar products to return
knn = KNNService(n_neighbors=10)

# Register routers for ETL and training triggers
app.include_router(etl_router)
app.include_router(train_router)


# Recommendation endpoint
@app.get("/recommend/{productid}")
def recommend(productid: int):
    """
    Returns KNN-based product recommendations for a given product ID.

    Parameters:
    - productid: ID of the product for which recommendations are requested

    Returns:
    - productid: requested product
    - recommendations: list of recommended product IDs
    """
    recs = knn.get_recommendations(productid)

    # If the product is not found or has no embedding, return 404
    if recs is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product {productid} not found"
        )
    # Successful response
    return {
        "productid": productid,
        "recommendations": recs
    }
