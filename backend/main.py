from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import uuid

from graph.workflow import app as workflow_app
from observability import setup_phoenix
import config

# Setup Phoenix
setup_phoenix()

# Create FastAPI app
app = FastAPI(
    title="Multi-City Trip Planner API",
    description="AI-powered country journey planner with LangGraph",
    version="2.0.0"
)

# CORS - allow all for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class TripRequest(BaseModel):
    country: str = Field(..., example="Japan")
    total_duration: int = Field(..., ge=3, le=30, example=14)
    interests: List[str] = Field(..., example=["temples", "food", "technology"])
    budget_tier: str = Field(..., pattern="^(budget|moderate|luxury)$", example="moderate")
    num_cities: Optional[int] = Field(None, ge=2, le=6)
    starting_city: Optional[str] = Field(None, example="Tokyo")
    travel_pace: str = Field(default="moderate", pattern="^(relaxed|moderate|fast)$")

# Routes
@app.get("/")
def root():
    return {
        "message": "Multi-City Trip Planner API",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "plan_trip": "POST /plan-trip",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "phoenix": "enabled"}

@app.post("/plan-trip")
async def plan_trip(request: TripRequest):
    """
    Generate multi-city trip plan

    This endpoint orchestrates 9 AI agents to create a comprehensive
    journey plan across multiple cities in a country.
    """
    try:
        # Prepare initial state
        initial_state = {
            "country": request.country,
            "total_duration": request.total_duration,
            "interests": request.interests,
            "budget_tier": request.budget_tier,
            "num_cities": request.num_cities,
            "starting_city": request.starting_city,
            "travel_pace": request.travel_pace,
            "messages": [],
            # Initialize all fields to avoid KeyError
            "country_overview": "",
            "best_months_to_visit": "",
            "visa_info": "",
            "safety_info": "",
            "recommended_cities": [],
            "city_route": [],
            "nights_per_city": {},
            "route_rationale": "",
            "transport_legs": [],
            "city_plans": [],
            "total_budget_estimate": 0.0,
            "budget_breakdown": {},
            "money_saving_tips": [],
            "packing_list": [],
            "travel_logistics": {},
            "final_response": {}
        }

        print(f"\n🌍 Planning trip to {request.country} for {request.total_duration} days...")

        # Run workflow with unique thread_id to avoid loading previous state
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        print(f"🔑 Using thread_id: {thread_id}")

        result = workflow_app.invoke(initial_state, config)

        print("✅ Trip plan generated successfully!")

        # Return final response
        return result.get("final_response", result)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Multi-City Trip Planner API Starting...")
    print("="*60)
    print(f"📍 API Server: http://localhost:8000")
    print(f"🔍 Phoenix UI: http://localhost:6006")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
