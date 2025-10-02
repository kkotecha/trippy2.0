# AI Trip Planner - Product Overview

## What It Is

An intelligent travel planning assistant that generates comprehensive, personalized trip itineraries using a multi-agent AI system powered by LangGraph. Users provide basic inputs (destination, interests, duration, budget), and the system orchestrates specialized AI agents to create detailed travel plans with budgets, accommodations, and local insights.

## Core Features

### User Inputs
- **Destination**: Any city or location worldwide
- **Interests**: Comma-separated activities (e.g., museums, food, nightlife, adventure)
- **Duration**: Number of days (1-30+)
- **Budget Level**: Budget, Moderate, or Luxury

### AI-Generated Outputs
- **Day-by-Day Itinerary**: Hour-by-hour activities with locations, timing, and costs
- **Budget Breakdown**: Detailed cost estimates for accommodation, food, transport, activities
- **Weather & Cultural Info**: Seasonal information, travel tips, cultural considerations
- **Accommodation Recommendations**: 3-5 specific hotels/hostels/Airbnbs with prices and neighborhoods
- **Transportation Guide**: Airport transfers, local transit, passes, costs, and apps
- **Local Insider Tips**: Hidden gems, safety info, money-saving tips, local customs

---

## Technical Architecture

### Tech Stack
- **Backend**: Python 3.9+, FastAPI, LangGraph, LangChain
- **AI Models**: OpenAI GPT-4o-mini (temperature: 0.7)
- **Frontend**: Vanilla HTML/CSS/JavaScript (static site, no build process)
- **Observability**: Arize Phoenix (local) or Arize AX Cloud (remote tracing)

### Multi-Agent System

The application uses **6 specialized AI agents** orchestrated by LangGraph in a **sequential execution pipeline**:

```
┌─────────────────────────────────────────────────────────────┐
│                        USER REQUEST                         │
│  destination: "Tokyo", interests: ["anime", "food"]         │
│  duration: 5 days, budget: "moderate"                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌───────────────────────┐
        │   1. RESEARCH AGENT   │  Weather, seasons, culture, safety
        │   (~10s)              │  → Updates: weather_info
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   2. BUDGET AGENT     │  Daily costs breakdown by category
        │   (~10s)              │  → Updates: budget_breakdown
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   3. ITINERARY AGENT  │  Day-by-day schedule with activities
        │   (~10s)              │  → Updates: itinerary
        └───────────┬───────────┘  (uses weather_info + budget_breakdown)
                    │
                    ▼
        ┌───────────────────────┐
        │ 4. ACCOMMODATION      │  Hotel/hostel/Airbnb recommendations
        │    AGENT (~9s)        │  → Updates: accommodation_suggestions
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ 5. TRANSPORTATION     │  Airport transfers, local transit
        │    AGENT (~7s)        │  → Updates: transportation_info
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ 6. LOCAL TIPS AGENT   │  Hidden gems, insider recommendations
        │    (~8s)              │  → Updates: local_tips
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ 7. COMPILER AGENT     │  Packages all data into final response
        │    (~1s)              │  → Updates: recommendations
        └───────────┬───────────┘
                    │
                    ▼
              ┌─────────────┐
              │   RESPONSE  │
              └─────────────┘
```

**Total Execution Time**: ~55-60 seconds (sequential)

### State Management

LangGraph uses a **TypedDict state** that flows through all agents:

```python
{
    "messages": [],                      # Conversation history
    "destination": "Tokyo",              # User input
    "interests": ["anime", "food"],      # User input
    "duration": 5,                       # User input
    "budget": "moderate",                # User input
    "weather_info": "",                  # Agent 1 output
    "budget_breakdown": "",              # Agent 2 output
    "itinerary": "",                     # Agent 3 output
    "accommodation_suggestions": "",     # Agent 4 output
    "transportation_info": "",           # Agent 5 output
    "local_tips": "",                    # Agent 6 output
    "recommendations": {}                # Agent 7 output (final)
}
```

**Key Concepts**:
1. **Sequential Execution**: Agents run in fixed order (1→2→3→4→5→6→7)
2. **State Accumulation**: Each agent reads previous outputs and adds new data
3. **Memory Persistence**: `MemorySaver()` tracks state for debugging and resumption
4. **LLM Specialization**: Each agent has a unique system prompt and role

### API Design

**Endpoint**: `POST /plan-trip`

**Request**:
```json
{
  "destination": "Paris",
  "interests": ["museums", "food", "nightlife"],
  "duration": 5,
  "budget": "moderate"
}
```

**Response**:
```json
{
  "destination": "Paris",
  "itinerary": "Day 1: Morning - Visit the Louvre...",
  "recommendations": {
    "weather_info": "Paris in October...",
    "budget_breakdown": "Total Budget: $2,000...",
    "accommodation": "1. Hotel Minerve (€120/night)...",
    "transportation": "From CDG Airport...",
    "local_tips": "Hidden gem: Musée Rodin gardens...",
    "interests": ["museums", "food", "nightlife"],
    "duration": 5,
    "budget": "moderate"
  }
}
```

### Frontend Architecture

**Tech**: Static HTML/CSS/JS (no framework, no build step)

**Features**:
- Responsive design with Tailwind CSS (via CDN)
- Tab-based results display (6 tabs)
- Loading states with spinner
- Error handling with retry functionality
- Markdown-style text formatting

**Tabs**:
1. **Itinerary** - Day-by-day schedule
2. **Budget** - Cost breakdown
3. **Accommodation** - Where to stay
4. **Transportation** - How to get around
5. **Weather & Tips** - Climate and general advice
6. **Local Insights** - Hidden gems and insider tips

### Observability & Tracing

**Phoenix (Local)**:
- Auto-launches at `http://localhost:6006`
- Traces all LLM calls and agent executions
- Shows token usage, latency, and costs
- Debugging tool for agent outputs

**Arize AX (Cloud)**:
- Production-grade tracing at `app.arize.com`
- Multi-environment support
- Advanced analytics and dashboards
- Configured via env vars: `ARIZE_SPACE_ID`, `ARIZE_API_KEY`

**What You Can See**:
- Full agent workflow visualization
- LLM prompt/response pairs
- Execution time per agent
- Token counts and API costs
- Error tracking and debugging

---

## Project Structure

```
trippy/
├── backend/
│   ├── main.py                 # FastAPI app (port 8000)
│   ├── agent.py                # Original 4-agent sequential system
│   ├── agent_parallel.py       # Enhanced 6-agent system (current)
│   ├── observability.py        # Phoenix/Arize setup
│   ├── requirements.txt        # Python dependencies
│   └── run_with_phoenix.sh     # Launch script with observability
├── frontend/
│   ├── index.html              # Main UI
│   ├── style.css               # Tailwind-based styling
│   └── script.js               # API communication and rendering
├── .env.example                # Environment variables template
├── .env                        # API keys (not in git)
├── README.md                   # Setup instructions
├── ARCHITECTURE.md             # Original architecture docs
├── PARALLEL_ARCHITECTURE.md    # Parallel execution notes
├── ARIZE_CLOUD_SETUP.md        # Cloud observability setup
└── OVERVIEW.md                 # This file
```

---

## Setup & Deployment

### Prerequisites
- Python 3.9+
- OpenAI API key
- (Optional) Arize account for cloud observability

### Quick Start

1. **Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
cp ../.env.example ../.env
# Edit .env and add: OPENAI_API_KEY=sk-...

# Run server
python main.py
```

Backend runs at: `http://localhost:8000`
Phoenix UI at: `http://localhost:6006`

2. **Frontend Setup**:
```bash
cd frontend
python3 -m http.server 3000
```

Frontend runs at: `http://localhost:3000`

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional (for cloud observability)
ARIZE_SPACE_ID=...
ARIZE_API_KEY=...
ARIZE_PROJECT_NAME=trip-planner
```

---

## Agent Details

### 1. Research Agent
**Role**: Travel Research Expert
**Purpose**: Gather destination intelligence
**Output**: Weather patterns, best visit times, cultural tips, safety info
**Context Used**: Destination only

### 2. Budget Agent
**Role**: Travel Budget Expert
**Purpose**: Calculate realistic costs
**Output**: Daily breakdown (accommodation, food, transport, activities, misc)
**Context Used**: Destination, duration, budget level, interests

### 3. Itinerary Agent
**Role**: Expert Travel Planner
**Purpose**: Create detailed schedule
**Output**: Day-by-day activities with times, locations, addresses, meal suggestions
**Context Used**: Weather info, budget constraints, interests

### 4. Accommodation Agent
**Role**: Accommodation Specialist
**Purpose**: Find places to stay
**Output**: 3-5 specific recommendations with prices, neighborhoods, booking tips
**Context Used**: Destination, duration, budget level

### 5. Transportation Agent
**Role**: Transportation Expert
**Purpose**: Plan how to get around
**Output**: Airport transfers, local transit options, passes, costs, apps
**Context Used**: Destination, budget level, duration

### 6. Local Tips Agent
**Role**: Local Expert
**Purpose**: Provide insider knowledge
**Output**: Hidden gems, restaurants, customs, safety, money-saving tips
**Context Used**: Destination, budget level, itinerary context

### 7. Compiler Agent
**Role**: Data Packager
**Purpose**: Structure final response
**Output**: JSON object with all agent outputs organized
**Context Used**: All previous agent outputs

---

## Performance Characteristics

- **Average Response Time**: 55-60 seconds (sequential execution)
- **LLM Calls**: 6 calls to GPT-4o-mini
- **Token Usage**: ~10,000-15,000 tokens per request
- **Cost**: ~$0.02-0.05 per trip plan (varies by OpenAI pricing)
- **Concurrency**: Single-threaded (sequential pipeline)

---

## Why LangGraph?

**Traditional Approach** (manual orchestration):
```python
weather = call_llm(research_prompt)
budget = call_llm(budget_prompt)
itinerary = call_llm(itinerary_prompt, weather, budget)
tips = call_llm(tips_prompt)
return compile(weather, budget, itinerary, tips)
```

**LangGraph Benefits**:
- ✅ **Automatic State Management**: No manual passing of data
- ✅ **Modularity**: Easy to add/remove/reorder agents
- ✅ **Type Safety**: TypedDict ensures data consistency
- ✅ **Observability**: Built-in tracing with Phoenix/Arize
- ✅ **Persistence**: Save/resume workflows with memory
- ✅ **Scalability**: Can add conditional routing, loops, parallelization
- ✅ **Debugging**: Inspect state at each step

---

## Alternative Implementation: Parallel Execution

The codebase includes `agent_parallel.py`, which was designed for parallel execution but currently runs sequentially due to state dependency constraints.

**Note from PARALLEL_ARCHITECTURE.md**: The parallel implementation promised 50% speed improvement (20-30s vs 45-60s) but the current implementation in `agent_parallel.py` actually runs sequentially with simple edge chaining, not true parallelization.

To switch to parallel agent (currently sequential in practice):
```python
# In main.py, line 7:
from agent_parallel import ParallelTripPlannerAgent as TripPlannerAgent
```

---

## Future Enhancements

### Performance
- [ ] Implement true parallel execution for independent agents
- [ ] Add streaming responses for real-time UI updates
- [ ] Cache destination research (weather data rarely changes)
- [ ] Implement rate limiting and request queuing

### Features
- [ ] Real-time weather API integration (vs LLM-generated)
- [ ] Hotel/flight booking system integration
- [ ] User authentication and trip saving
- [ ] Map visualization of itinerary
- [ ] Export to PDF/Calendar formats
- [ ] Multi-language support
- [ ] Image generation for destinations

### New Agents
- [ ] Restaurant reservation agent
- [ ] Activity booking agent (check availability)
- [ ] Packing list generator
- [ ] Language/phrase helper
- [ ] Photography spots recommender

### Architecture
- [ ] Conditional routing based on destination type (city vs nature)
- [ ] Adaptive agent selection (luxury → add fine dining agent)
- [ ] Human-in-the-loop approval steps
- [ ] Multi-destination trip planning
- [ ] Collaborative planning (multiple users)

---

## Known Limitations

1. **No Real-Time Data**: Weather and prices are LLM estimates, not live APIs
2. **Sequential Execution**: Despite parallel agent code, runs sequentially
3. **No Booking Integration**: Recommendations only, no direct booking
4. **Limited Error Handling**: Network failures may not retry gracefully
5. **No User Accounts**: Cannot save or retrieve past trips
6. **OpenAI Dependency**: Requires API key and is subject to rate limits
7. **Static Frontend**: No framework, limited interactivity

---

## Monitoring & Debugging

### Phoenix Dashboard (Local)
Access: `http://localhost:6006`

**Key Metrics**:
- Trace timeline (which agent is running)
- LLM token usage per agent
- Latency per agent and overall
- Error rates and failure messages
- Prompt/response inspection

### Arize AX (Cloud)
Access: `https://app.arize.com/`

**Key Features**:
- Production tracing across multiple sessions
- Cost tracking and analytics
- Performance degradation alerts
- Model comparison (if testing different LLMs)

### Logging
FastAPI logs all requests to console:
```bash
INFO:     127.0.0.1:52341 - "POST /plan-trip HTTP/1.1" 200 OK
```

---

## Security Considerations

1. **API Key Management**: Store `OPENAI_API_KEY` in `.env`, never commit
2. **CORS**: Currently allows all origins (`allow_origins=["*"]`) - restrict in production
3. **Rate Limiting**: No rate limiting implemented - vulnerable to abuse
4. **Input Validation**: Basic validation via Pydantic models
5. **Error Messages**: May leak internal details in error responses

---

## License

MIT

---

## Contact & Support

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: See README.md for setup details
- **Observability**: Phoenix docs at `docs.arize.com/phoenix`
