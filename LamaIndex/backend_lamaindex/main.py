# main.py

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from agent import MultiAgentManager

app = FastAPI()
manager = MultiAgentManager()

@app.get("/health")
def health_check() -> JSONResponse:
    return JSONResponse({
        "status": status.HTTP_200_OK,
        "message": "API is running."
    })

"""
This file sets up a simple FastAPI server, defining a `/health` endpoint
to check API availability and initializing the `MultiAgentManager` for further routes.
"""
