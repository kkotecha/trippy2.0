# Quick Start Guide - Multi-City Trip Planner

## Step-by-Step Setup

### 1. Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# Required: OPENAI_API_KEY=sk-your-actual-key-here
```

### 2. Install Backend Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the Backend

```bash
# Make sure you're in the backend directory with venv activated
python main.py
```

You should see:
```
✅ Config loaded: gpt-4o-mini, Environment: development
🏠 Using local Phoenix...
✅ Local Phoenix: http://localhost:6006
✅ Phoenix observability enabled
🚀 Multi-City Trip Planner API Starting...
📍 API Server: http://localhost:8000
🔍 Phoenix UI: http://localhost:6006
📚 API Docs: http://localhost:8000/docs
```

### 4. Start the Frontend (New Terminal)

```bash
cd frontend
python3 -m http.server 3000
```

### 5. Test the Application

Open your browser to: http://localhost:3000

**Example Input:**
- Country: Japan
- Duration: 10 days
- Interests: temples, food, technology
- Budget: Moderate
- Travel Pace: Moderate

Click "Plan My Journey 🚀" and wait 60-90 seconds.

### 6. Monitor with Phoenix

While the trip is being planned, open: http://localhost:6006

You'll see real-time traces of:
- All 9 agents executing
- Tool calls (web search, route optimization, etc.)
- LLM interactions
- Token usage and costs

## Architecture Overview

```
User Request
    ↓
FastAPI Endpoint (/plan-trip)
    ↓
LangGraph Workflow (Sequential Execution)
    ↓
├─ Agent 1: Country Research (web_search, visa_info)
├─ Agent 2: Route Planning (optimize_route, web_search)
├─ Agent 3: Transport (search_trains)
├─ Agent 4-6: City Processing Loop
│   ├─ Accommodation (search_hotels)
│   ├─ Itinerary (search_attractions)
│   └─ Local Transport
├─ Agent 7: Budget Compilation
├─ Agent 8: Logistics (packing, visas)
└─ Agent 9: Final Compiler
    ↓
JSON Response → Frontend
    ↓
Dynamic Tabs Display
```

## Key Files

- `backend/main.py` - FastAPI app entry point
- `backend/graph/workflow.py` - LangGraph agent orchestration
- `backend/agents/` - 9 specialized agent implementations
- `backend/tools/` - 15+ tool functions
- `frontend/script.js` - Frontend logic and rendering

## Troubleshooting

### "Module not found" errors
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### OpenAI API errors
- Check `.env` file exists and has valid `OPENAI_API_KEY`
- Verify API key at: https://platform.openai.com/api-keys
- Check you have credits available

### Phoenix not showing traces
- Visit http://localhost:6006 in a new tab
- Ensure observability.py is being imported in main.py
- Check terminal for Phoenix startup logs

## Next Steps

1. **Try different countries**: Italy, France, Thailand, Spain
2. **Experiment with parameters**: Budget tiers, travel pace, number of cities
3. **View traces in Phoenix**: Understand agent decision-making
4. **Customize agents**: Modify prompts in `backend/agents/`
5. **Add new tools**: Create tools in `backend/tools/`

## Performance Notes

- **Expected response time**: 60-90 seconds for full journey
- **Bottlenecks**: City processing (sequential), web searches
- **Optimization opportunities**: Parallel city processing, caching, faster models

Enjoy planning your multi-city adventures! 🌍✈️
