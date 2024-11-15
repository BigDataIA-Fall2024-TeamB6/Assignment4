
from fastapi import FastAPI
from dotenv import load_dotenv
import logging
from routers import router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Include router
app.include_router(router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Endpoint for health check"""
    return {"status": "Healthy", "message": "FastAPI is running smoothly"}
