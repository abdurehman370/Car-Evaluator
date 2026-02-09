from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import logging
import os

from dubizzle_client import DubizzleClient
from filters import QueryBuilder
from exporter import Exporter
from evaluator import PriceEvaluator
from config import PRIMARY_INDEX, DEFAULT_HITS_PER_PAGE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Dubizzle Scraper API")

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class ScrapeRequest(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    mileage_max: Optional[int] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    max_pages: int = 1
    use_proxy: bool = False
    proxy: Optional[str] = None

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/api/scrape")
async def scrape_listings(req: ScrapeRequest):
    logger.info(f"Received scrape request: {req}")
    
    client = DubizzleClient(proxy=req.proxy if req.use_proxy else None)
    all_results = []
    
    try:
        for page in range(req.max_pages):
            # Build payload using QueryBuilder
            # We need to adapt QueryBuilder to take our pydantic model or mock args
            class MockArgs:
                pass
            args = MockArgs()
            args.make = req.make
            args.model = req.model
            args.year_min = req.year_min
            args.year_max = req.year_max
            args.mileage_max = req.mileage_max
            args.price_min = req.price_min
            args.price_max = req.price_max
            
            payload = QueryBuilder.build_payload(
                args, 
                page=page, 
                hits_per_page=DEFAULT_HITS_PER_PAGE,
                index_name=PRIMARY_INDEX
            )
            
            hits, nb_pages, total_hits = client.get_listings(payload)
            
            if not hits:
                break
                
            for hit in hits:
                all_results.append(Exporter.format_listing(hit))
                
                
            if page + 1 >= nb_pages:
                break
        
        evaluation = PriceEvaluator.calculate_stats(all_results)
                
        return {
            "status": "success",
            "total_results": len(all_results),
            "data": all_results,
            "evaluation": evaluation
        }
        
    except Exception as e:
        logger.error(f"Scrape error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
