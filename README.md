# Multi-City Trip Planner 🌍

AI-powered country journey planner using LangGraph's multi-agent architecture with Arize Phoenix observability.

## Features

- 🗺️ **Multi-city route optimization** - Plan journeys across 2-6 cities
- 🚆 **Inter-city transportation** - Trains, buses, flights with costs
- 🏨 **Accommodation recommendations** - Hotels, hostels, Airbnbs
- 📅 **Day-by-day itineraries** - Activities, meals, timing, costs
- 💰 **Budget breakdowns** - Complete cost estimates by category
- 🎒 **Travel logistics** - Packing lists, visas, local tips
- 🔍 **Full observability** - Arize Phoenix tracing of all agents

## Architecture

### 9 Specialized Agents

1. **Country Research Agent** - Destination intelligence
2. **Route Planning Agent** - Optimal city ordering
3. **Transport Agent** - Inter-city travel options
4. **Accommodation Agent** - Where to stay (per city)
5. **Itinerary Agent** - Daily activities (per city)
6. **Local Transport Agent** - Getting around (per city)
7. **Budget Compiler** - Financial breakdown
8. **Logistics Agent** - Packing and preparation
9. **Compiler Agent** - Final JSON response

### 15+ Tools

- `web_search` - Real-time web search via Tavily
- `optimize_route` - TSP algorithm for minimal travel
- `calculate_travel_time` - Geocoding + distance
- `search_hotels` - Accommodation options
- `search_trains` - Train routes and costs
- `search_attractions` - Tourist activities
- `get_visa_requirements` - Entry requirements
- And more...

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- (Optional) Tavily API key for web search

### Installation

```bash
# Clone repository (or navigate to your project directory)
cd trippy2.0

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cd ..
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Application

```bash
# Terminal 1: Run backend
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

Backend runs at:
- API: http://localhost:8000
- Phoenix UI: http://localhost:6006
- API Docs: http://localhost:8000/docs

```bash
# Terminal 2: Run frontend
cd frontend
python3 -m http.server 3000
```

Visit: http://localhost:3000

## Usage Example

### Input:
```json
{
  "country": "Japan",
  "total_duration": 14,
  "interests": ["temples", "food", "technology"],
  "budget_tier": "moderate",
  "starting_city": "Tokyo",
  "travel_pace": "moderate"
}
```

### Output:
- Route: Tokyo (4 nights) → Kyoto (4 nights) → Osaka (3 nights) → Hiroshima (3 nights)
- 3 hotels per city with prices
- Day-by-day activities for each city
- Train connections with costs
- Total budget: ~$3,500

## Observability

### Local Phoenix
Automatically starts at http://localhost:6006

View:
- Agent execution graph
- Tool calls and results
- LLM prompts and responses
- Token usage and costs
- Execution timeline

### Arize Cloud (Optional)
Add to `.env`:
```
ARIZE_SPACE_ID=your-space-id
ARIZE_API_KEY=your-api-key
```

View at: https://app.arize.com

## Project Structure

```
backend/
├── main.py              # FastAPI app
├── agents/              # 9 agent implementations
├── tools/               # 15+ tool functions
├── graph/               # LangGraph workflow
├── config.py            # Configuration
└── observability.py     # Phoenix setup

frontend/
├── index.html           # Form + dynamic tabs
├── script.js            # API calls + rendering
└── style.css            # Styling
```

## Development

### Adding a New Tool

```python
# backend/tools/your_tool.py
from langchain_core.tools import tool

@tool
def your_new_tool(param: str) -> dict:
    """Tool description for LLM"""
    # Implementation
    return {"result": "data"}
```

### Adding a New Agent

```python
# backend/agents/your_agent.py
from graph.state import TripPlannerState

def your_agent_node(state: TripPlannerState) -> dict:
    """Agent implementation"""
    # Use tools, call LLM
    return {"new_state_field": "value"}
```

Update workflow in `backend/graph/workflow.py`

## Troubleshooting

### Phoenix not starting:
```bash
# Kill existing Phoenix process
pkill -f phoenix
python main.py
```

### Tool errors:
- Check API keys in .env
- Verify network connection
- Check Phoenix UI for error traces

### Slow responses:
- Expected: 60-90 seconds for full journey
- Check Phoenix UI for bottleneck agents
- Consider using faster LLM model

## Future Enhancements

- [ ] Parallel city processing (20-30s response time)
- [ ] Real booking API integration
- [ ] Interactive map visualization
- [ ] PDF export
- [ ] User authentication
- [ ] Trip saving/loading

## License

MIT

## Credits

Built with:
- LangGraph
- LangChain
- Arize Phoenix
- FastAPI
