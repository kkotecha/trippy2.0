from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from observability import setup_observability
from agent import TripPlannerAgent

# Setup observability (Phoenix or Arize Cloud)
setup_observability()

app = FastAPI(title="Trip Planner API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the trip planner agent
trip_agent = TripPlannerAgent()

class TripRequest(BaseModel):
    destination: str
    interests: List[str]
    duration: int  # number of days
    budget: Optional[str] = "moderate"

class TripResponse(BaseModel):
    destination: str
    itinerary: str
    recommendations: dict

@app.get("/")
async def root():
    return {"message": "Trip Planner API", "status": "running"}

@app.post("/plan-trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    """
    Plan a trip based on destination, interests, duration, and budget
    """
    try:
        result = trip_agent.plan_trip(
            destination=request.destination,
            interests=request.interests,
            duration=request.duration,
            budget=request.budget
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)