# Multi-City Trip Planner 🌍

AI-powered country journey planner using LangGraph's multi-agent architecture with Arize Phoenix Cloud observability.

> ⚠️ **Project Status:** This is a functional prototype with mixed real and mock data. See [Tool Status](#tool-status-real-vs-mock-data) below for details on which features use real APIs vs placeholder data.

## Features

- 🗺️ **Multi-city route optimization** - Plan journeys across 2-6 cities
- 🚆 **Inter-city transportation** - Train/bus routes (mock data, see status below)
- 🏨 **Accommodation recommendations** - Hotel suggestions (mock data, see status below)
- 📅 **Day-by-day itineraries** - Activities and attractions (mock data, see status below)
- 💰 **Budget breakdowns** - Complete cost estimates
- 🎒 **Travel logistics** - Packing lists, visas, local tips
- 🔍 **Full observability** - Arize Phoenix Cloud tracing of all agents and LLM calls

## Architecture

### 9 Specialized Agents

| Agent | Purpose | Status |
|-------|---------|--------|
| 1. **Country Research Agent** | Destination intelligence, visa, currency info | ✅ Functional |
| 2. **Route Planning Agent** | Optimal city ordering and route optimization | ✅ Functional |
| 3. **Transport Agent** | Inter-city travel options (trains/buses) | ⚠️ Uses mock data |
| 4. **Accommodation Agent** | Hotel/hostel recommendations per city | ⚠️ Uses mock data |
| 5. **Itinerary Agent** | Daily activities and attractions per city | ⚠️ Uses mock data |
| 6. **Local Transport Agent** | Getting around within cities | ✅ Functional |
| 7. **Budget Compiler** | Financial breakdown and cost estimates | ✅ Functional |
| 8. **Logistics Agent** | Packing lists and travel preparation | ✅ Functional |
| 9. **Compiler Agent** | Final structured JSON response | ✅ Functional |

### Tool Status: Real vs Mock Data

#### ✅ FULLY DYNAMIC TOOLS (Real Data)

| Tool | Description | Data Source |
|------|-------------|-------------|
| `web_search` | Real-time web search | **Tavily API** |
| `optimize_route` | City route optimization using TSP | **Geopy + OpenStreetMap Nominatim** |

#### ⚠️ PARTIALLY DYNAMIC TOOLS

| Tool | Description | Status |
|------|-------------|--------|
| `calculate_travel_time` | Travel time between cities | Uses real geocoding but assumes fixed 80 km/h speed (not realistic) |

#### ❌ MOCK/DUMMY TOOLS (Need API Integration)

| Tool | Description | Current Behavior | Needed API |
|------|-------------|------------------|------------|
| `search_hotels` | Hotel recommendations | Returns generic mock hotels like "{City} Central Hotel" with estimated prices | Booking.com API, Google Places API |
| `search_trains` | Train/bus routes | Hardcoded data for only 3 routes (Tokyo-Kyoto, Kyoto-Osaka, Paris-Lyon) | Rome2Rio API, Trainline API |
| `search_attractions` | Tourist attractions | Returns 4 generic mock attractions per city | Google Places API, TripAdvisor API |
| `get_visa_requirements` | Visa information | Hardcoded info for only 4 countries (Japan, Italy, Thailand, France) | Sherpa API, VisaDB API |
| `get_currency_info` | Currency and exchange info | Hardcoded data for 4 countries | RestCountries API + ExchangeRate API |

> 📋 **See [TOOL_IMPROVEMENT_ANALYSIS.md](backend/TOOL_IMPROVEMENT_ANALYSIS.md)** for detailed recommendations on making each tool dynamic with real APIs.

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key (required)
- Tavily API key (optional, for web search)
- Arize Phoenix account (optional, for cloud observability)

### Installation

```bash
# Clone repository
cd trippy2.0

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your keys:
#   - OPENAI_API_KEY (required)
#   - TAVILY_API_KEY (optional but recommended)
#   - ARIZE_SPACE_ID and ARIZE_API_KEY (optional)
```

### Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Optional - Web Search (highly recommended for better results)
TAVILY_API_KEY=tvly-your-tavily-api-key

# Optional - Arize Phoenix Cloud Observability
ARIZE_SPACE_ID=your-space-id
ARIZE_API_KEY=your-api-key
ARIZE_PROJECT_NAME=trippy-multi-city

# App Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.5
```

### Running the Application

```bash
# Terminal 1: Run backend
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

Backend runs at:
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Interactive Swagger UI)
- **Arize Phoenix:** https://app.arize.com (if configured)

```bash
# Terminal 2: Run frontend
cd frontend
python3 -m http.server 3000
```

Visit: **http://localhost:3000**

## Usage Example

### Input:
```json
{
  "country": "Japan",
  "total_duration": 14,
  "interests": ["temples", "food", "technology"],
  "budget_tier": "moderate",
  "starting_city": "Tokyo",
  "travel_pace": "moderate",
  "num_cities": 4
}
```

### Output:
```json
{
  "country_overview": "Detailed Japan overview...",
  "city_route": ["Tokyo", "Kyoto", "Osaka", "Hiroshima"],
  "nights_per_city": {
    "Tokyo": 4,
    "Kyoto": 4,
    "Osaka": 3,
    "Hiroshima": 3
  },
  "transport_legs": [
    {
      "from": "Tokyo",
      "to": "Kyoto",
      "method": "Shinkansen (bullet train)",
      "duration": "2h 15min",
      "cost": "$130"
    }
  ],
  "city_plans": [
    {
      "city": "Tokyo",
      "hotels": [...],  // Mock data
      "itinerary": [...],  // Mock data
      "local_transport": {...}
    }
  ],
  "total_budget_estimate": 3500,
  "budget_breakdown": {...},
  "packing_list": [...],
  "travel_logistics": {...}
}
```

> ⚠️ Note: Hotels, attractions, and most transport data are currently mock/placeholder values. See [Tool Status](#tool-status-real-vs-mock-data) above.

## Observability with Arize Phoenix Cloud

This project includes full observability using **Arize Phoenix Cloud** to trace:
- All 9 agent executions
- LLM calls with prompts and responses
- Tool invocations and results
- Token usage and costs
- Execution timeline and dependencies

### Setup Arize Phoenix

1. **Sign up** at https://app.arize.com
2. **Create a project** or use existing space
3. **Get credentials:**
   - Space ID from space settings
   - API Key from space settings
4. **Add to `.env`:**
   ```bash
   ARIZE_SPACE_ID=your-space-id
   ARIZE_API_KEY=your-api-key
   ARIZE_PROJECT_NAME=trippy-multi-city
   ```
5. **Restart backend** - traces will appear in Arize dashboard

### What You'll See in Phoenix

- 🔍 Complete agent workflow graph
- 📊 LLM token usage and costs
- ⏱️ Performance bottlenecks
- 🛠️ Tool success/failure rates
- 🔗 Full trace of each request through all 9 agents

View traces at: **https://app.arize.com**

## Project Structure

```
trippy2.0/
├── README.md                          # This file
├── backend/
│   ├── main.py                        # FastAPI application entry point
│   ├── config.py                      # Configuration and environment variables
│   ├── observability.py               # Arize Phoenix Cloud setup
│   ├── requirements.txt               # Python dependencies
│   ├── TOOL_IMPROVEMENT_ANALYSIS.md   # Detailed tool improvement roadmap
│   │
│   ├── agents/                        # 9 specialized agents
│   │   ├── country_research.py        # Agent 1: Destination intelligence
│   │   ├── route_planning.py          # Agent 2: City route optimization
│   │   ├── transport.py               # Agent 3: Inter-city transport
│   │   ├── accommodation.py           # Agent 4: Hotels per city
│   │   ├── itinerary.py               # Agent 5: Daily activities per city
│   │   ├── local_transport.py         # Agent 6: Getting around cities
│   │   ├── budget.py                  # Agent 7: Cost compilation
│   │   ├── logistics.py               # Agent 8: Packing and prep
│   │   └── compiler.py                # Agent 9: Final response builder
│   │
│   ├── tools/                         # Tool implementations
│   │   ├── __init__.py                # Tool exports
│   │   ├── search_tools.py            # ✅ web_search (Tavily)
│   │   ├── calculation_tools.py       # ✅ optimize_route, ⚠️ calculate_travel_time
│   │   ├── hotel_tools.py             # ❌ search_hotels (mock)
│   │   ├── transport_tools.py         # ❌ search_trains (mock)
│   │   ├── attraction_tools.py        # ❌ search_attractions (mock)
│   │   └── knowledge_tools.py         # ❌ visa/currency (mock)
│   │
│   └── graph/                         # LangGraph workflow
│       ├── state.py                   # State definitions (TripPlannerState, CityState)
│       └── workflow.py                # Agent orchestration graph
│
└── frontend/
    ├── index.html                     # Trip planner form UI
    ├── script.js                      # API calls and result rendering
    └── style.css                      # Styling
```

## Development

### Adding a New Tool

1. Create tool in `backend/tools/your_tool.py`:

```python
from langchain_core.tools import tool

@tool
def your_new_tool(param: str) -> dict:
    """
    Tool description that the LLM will see.
    Be specific about what it does and when to use it.
    """
    # Implementation with error handling
    try:
        result = your_api_call(param)
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}
```

2. Export in `backend/tools/__init__.py`
3. Import and use in relevant agent

### Adding a New Agent

1. Create agent in `backend/agents/your_agent.py`:

```python
from graph.state import TripPlannerState
from langchain_openai import ChatOpenAI
from tools import your_tool

def your_agent_node(state: TripPlannerState) -> dict:
    """Agent implementation with LLM and tools"""
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Use tools and LLM to process state
    result = your_tool.invoke({"param": state["field"]})

    return {"new_field": result}
```

2. Update `backend/graph/state.py` to add new state fields
3. Add node to workflow in `backend/graph/workflow.py`

### Upgrading Mock Tools to Real APIs

See **[TOOL_IMPROVEMENT_ANALYSIS.md](backend/TOOL_IMPROVEMENT_ANALYSIS.md)** for:
- Detailed analysis of each mock tool
- Recommended APIs with links
- Implementation priorities
- Cost considerations
- Code examples

**Priority order:**
1. `search_hotels` → Booking.com API or Google Places
2. `search_attractions` → Google Places or TripAdvisor
3. `search_trains` → Rome2Rio or Trainline API

## Troubleshooting

### Backend won't start

```bash
# Ensure you're in venv
cd backend
source venv/bin/activate

# Check dependencies
pip install -r requirements.txt

# Verify .env file exists and has OPENAI_API_KEY
cat .env
```

### Arize Phoenix Cloud not connecting

```bash
# Check credentials in .env
ARIZE_SPACE_ID=...  # Should be base64 encoded string
ARIZE_API_KEY=...   # Should start with "ak-"

# Verify credentials at https://app.arize.com space settings
# Check backend logs for connection errors
```

### Tool errors during execution

- Check `.env` has all required API keys
- Verify network connection
- Check Arize Phoenix dashboard for detailed error traces
- Look at backend console logs for specific tool failures

### Slow responses

- **Expected:** 60-90 seconds for full multi-city journey
- **Normal bottlenecks:**
  - Country research (web search): 5-10s
  - Each city itinerary planning: 8-12s per city
  - Route optimization with 4+ cities: 5-8s
- **Check:** Arize Phoenix timeline view to identify slow agents
- **Optimization:** Consider using `gpt-4o-mini` (current) vs `gpt-4` for speed

## API Response Times

Typical execution breakdown for 4-city, 14-day trip:

| Agent | Time | Reason |
|-------|------|--------|
| Country Research | 10-15s | Web search + LLM processing |
| Route Planning | 5-8s | Geocoding + optimization |
| Transport | 3-5s | Mock data lookup |
| City Planning (×4) | 40-50s | LLM generates itinerary per city |
| Budget | 3-5s | Aggregation |
| Logistics | 3-5s | Packing list generation |
| Compiler | 2-3s | JSON assembly |
| **Total** | **65-90s** | End-to-end |

## Roadmap

### Short Term (Mock → Real Data)
- [ ] Integrate Booking.com API for real hotel data
- [ ] Add Google Places API for real attractions
- [ ] Implement Rome2Rio API for actual transport routes
- [ ] Add Sherpa API for up-to-date visa requirements
- [ ] Integrate ExchangeRate API for currency data

### Medium Term (Features)
- [ ] Parallel city processing (reduce to 20-30s response time)
- [ ] Interactive map visualization with route overlay
- [ ] PDF export of complete itinerary
- [ ] Save/load trip plans
- [ ] User authentication and trip history

### Long Term (Advanced)
- [ ] Real booking integration (book hotels/trains directly)
- [ ] Multi-country trips (e.g., Thailand + Vietnam)
- [ ] Collaborative trip planning (multiple users)
- [ ] Mobile app with offline itinerary access
- [ ] AI-powered trip modifications ("Add one more day in Kyoto")

## Contributing

Contributions welcome! Priority areas:
1. **Upgrading mock tools** - See TOOL_IMPROVEMENT_ANALYSIS.md
2. **Performance optimization** - Parallel agent execution
3. **Frontend improvements** - Map view, better visualizations
4. **Testing** - Unit tests for agents and tools

## Known Limitations

⚠️ **Data Accuracy:**
- Hotel, attraction, and transport data are currently mock/placeholder
- Prices are estimates based on tier, not real-time data
- Train routes limited to 3 hardcoded examples
- Visa info hardcoded for 4 countries only

⚠️ **Performance:**
- Sequential agent execution (60-90s response time)
- No caching of repeated city lookups
- Rate limited by Nominatim geocoding (1 req/sec)

⚠️ **Functionality:**
- No user authentication or data persistence
- Cannot modify generated plans
- Limited to single-country trips
- Max 6 cities per trip

## License

MIT License - feel free to use and modify for your own projects.

## Credits

Built with:
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Multi-agent orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** - LLM framework
- **[Arize Phoenix](https://phoenix.arize.com/)** - AI observability platform
- **[FastAPI](https://fastapi.tiangolo.com/)** - Backend framework
- **[OpenAI GPT-4o-mini](https://openai.com/)** - Language model
- **[Tavily](https://tavily.com/)** - Web search API
- **[Geopy](https://geopy.readthedocs.io/)** - Geocoding and route optimization

---

**Built by:** [Your Name]
**Last Updated:** October 2, 2025
**Version:** 2.0.0 (Functional Prototype)
