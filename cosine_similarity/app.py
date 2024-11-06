from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
import uvicorn
from fashion_recommender import FashionRecommender

# Initialize FastAPI app
app = FastAPI(title="Fashion Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset and initialize recommender
print("Loading dataset...")
try:
    df = pd.read_csv('../dataset/Fashion Dataset.csv')
    print(f"Successfully loaded dataset with {len(df)} items")
except Exception as e:
    print(f"Error loading dataset: {e}")
    raise

print("Initializing recommender...")
recommender = FashionRecommender(df)
print("Recommender initialized successfully")

class SearchQuery(BaseModel):
    query: str
    page_size: int = 5
    page: int = 1

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Fashion Search API is running",
        "dataset_size": len(df),
        "endpoints": {
            "root": "GET /",
            "search": "POST /search"
        }
    }

@app.post("/search")
async def search_products(search_query: SearchQuery):
    try:
        print(f"Received search query: {search_query.query}, page: {search_query.page}")
        
        # Calculate total results needed
        total_results = search_query.page * search_query.page_size
        
        # Get results
        results = recommender.search_similar_items(
            search_query.query, 
            n_results=total_results
        )
        
        # Calculate if there are more results available
        has_more = len(results) == total_results
        
        print(f"Found {len(results)} results")
        return {
            "results": results,
            "has_more": has_more,
            "current_page": search_query.page
        }
    except Exception as e:
        print(f"Error processing search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# This is critical for starting the server
if __name__ == "__main__":
    print("Starting Fashion Search API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
