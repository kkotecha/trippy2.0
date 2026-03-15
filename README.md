# Trippy 2.0 — Multi-City AI Trip Planner (Prototype)

An AI-powered multi-city journey planner that uses 9 specialized LangGraph agents to generate comprehensive travel itineraries across 2-6 cities in a single country.

**Part of a 3-project series:** See [Trippy v1](https://github.com/kkotecha/trippy) (foundations) and [Trippy 3.0](https://github.com/kkotecha/trippy3.0) (production with real APIs).

## Why This Version Exists

Trippy v1 proved that agent decomposition works for trip planning. v2.0 tackles the next set of product and engineering challenges:

- **Multi-city coordination:** How do you plan across multiple cities with route optimization?
- **Tool integration:** How do agents call external tools (search, geocoding) alongside LLM reasoning?
- **Mock → Real migration path:** How do you architect tools so mock implementations can be swapped for real APIs without changing agent logic?

The core question: **How do you design a multi-agent system with a clean tool abstraction layer that lets you iterate from prototype to production incrementally?**

## What Changed from v1

| Aspect | v1 | v2.0 |
|--------|-----|------|
| Scope | Single city | 2-6 cities in one country |
| Agents | 4 | 9 (new: route planning, transport, accommodation, budget, logistics) |
| Tools | None (LLM-only) | 7 tools (2 real, 5 mock) |
| Route Planning | N/A | TSP optimization with Geopy + OpenStreetMap |
| State | Simple flat dict | Nested TypedDict with CityState sub-objects |
| Observability | Local Phoenix | Arize Phoenix Cloud |

## Architecture

```
[User Input: country, cities, duration, interests, budget]
     │
     ▼
┌─────────────────────┐
│ 1. Country Research  │  ← Tavily web search (real)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 2. Route Planning    │  ← Geopy + OSM geocoding (real)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 3. Transport         │  ← Inter-city routes (mock)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 4-6. City Processing │  ← Per-city loop: hotels, itinerary, local transport (mock)
│      (per city)      │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 7. Budget Compiler   │  ← Aggregates all costs
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 8. Logistics         │  ← Packing, visas, currency (mock)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 9. Compiler          │  ← Final structured JSON
└────────┬────────────┘
         ▼
   [Complete Trip Plan]
```

### Tool Status: Real vs Mock

| Tool | Source | Status |
|------|--------|--------|
| `web_search` | Tavily API | Real |
| `optimize_route` | Geopy + OSM | Real |
| `search_hotels` | Hardcoded mock | Mock |
| `search_trains` | 3 hardcoded routes | Mock |
| `search_attractions` | Generic mock | Mock |
| `get_visa_requirements` | 4 countries only | Mock |
| `get_currency_info` | 4 currencies only | Mock |

This is intentional — the mock tools define the interface contract. Swapping them for real APIs (done in v3.0) requires zero changes to agent logic.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| Agent Orchestration | LangGraph + LangChain |
| LLM | OpenAI GPT-4o-mini |
| Real Tools | Tavily (search), Geopy (geocoding) |
| Observability | Arize Phoenix Cloud |
| Frontend | HTML, Tailwind CSS, Vanilla JS |

## Key Concepts Explored

**1. Tool Abstraction Layer**
Each tool is a `@tool`-decorated function with a clear interface. Mock tools return hardcoded data in the exact format real APIs would return. This means swapping `search_hotels` from mock → Google Places API requires changing only the tool implementation — agents, state, and graph remain untouched.

**2. Nested State Management**
v1's flat state doesn't scale to multi-city. v2.0 introduces `CityState` as a sub-object within `TripPlannerState`, with per-city hotels, itineraries, and transport. This pattern applies to any multi-entity workflow.

**3. Route Optimization**
The route planner uses a TSP (Travelling Salesman Problem) approach with Geopy geocoding to minimize backtracking across cities. This demonstrates how agents can combine LLM reasoning with algorithmic computation.

**4. Mock-to-Real Migration**
The `TOOL_IMPROVEMENT_ANALYSIS.md` documents exactly which APIs to use, cost implications, and implementation priority for each mock tool. This is the kind of product roadmap artifact that bridges prototype to production.

## Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API key (required)
- Tavily API key (optional, for web search)

### Setup

```bash
git clone https://github.com/kkotecha/trippy2.0.git
cd trippy2.0/backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add: OPENAI_API_KEY (required), TAVILY_API_KEY (optional)

python main.py
# API at http://localhost:8000
```

```bash
# Frontend (separate terminal)
cd frontend
python3 -m http.server 3000
# Visit http://localhost:3000
```

## For Practitioners: How to Use This Repo

If you've already explored v1 (or understand basic LangGraph), this repo teaches you the next level.

**Step 1: Compare agent.py (v1) with agents/ directory (v2)**
v1 has all agents in one file. v2 splits them into separate modules — see how `backend/agents/` organizes 9 agents and how `backend/graph/workflow.py` wires them together. This is the pattern for production-grade agent systems.

**Step 2: Study the tool layer**
Open any file in `backend/tools/`. Notice how `search_hotels` returns structured data even as a mock. Now read `TOOL_IMPROVEMENT_ANALYSIS.md` to see the real API that would replace it. The interface stays the same.

**Step 3: Trace the state through all 9 agents**
Open `backend/graph/state.py` — the `TripPlannerState` TypedDict has fields for each agent's output. Follow how state accumulates as it flows through the graph. This is the backbone of multi-agent coordination.

**Step 4: Swap a mock tool for a real one**
Pick `get_currency_info` (simplest) and replace the hardcoded data with a call to [ExchangeRate-API](https://www.exchangerate-api.com/) (free, no key needed). This exercise teaches you the mock→real migration pattern.

**Then move to [Trippy 3.0](https://github.com/kkotecha/trippy3.0)** — where all tools are real, the system is deployed, and production concerns (CORS, deployment, rate limits) are addressed.

## Project Structure

```
trippy2.0/
├── backend/
│   ├── main.py                        # FastAPI entry point
│   ├── config.py                      # Environment config
│   ├── observability.py               # Arize Phoenix Cloud
│   ├── agents/                        # 9 specialized agents
│   │   ├── country_research.py
│   │   ├── route_planning.py
│   │   ├── transport.py
│   │   ├── city_processing.py         # Per-city loop (hotels, itinerary, local transport)
│   │   ├── budget.py
│   │   ├── logistics.py
│   │   └── compiler.py
│   ├── tools/                         # Tool implementations (mock + real)
│   │   ├── search_tools.py            # web_search (Tavily - real)
│   │   ├── calculation_tools.py       # optimize_route (Geopy - real)
│   │   ├── hotel_tools.py             # search_hotels (mock)
│   │   ├── transport_tools.py         # search_trains (mock)
│   │   ├── attraction_tools.py        # search_attractions (mock)
│   │   └── knowledge_tools.py         # visa/currency (mock)
│   ├── graph/
│   │   ├── state.py                   # TripPlannerState + CityState
│   │   └── workflow.py                # LangGraph workflow definition
│   └── TOOL_IMPROVEMENT_ANALYSIS.md   # Mock → real API roadmap
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
└── README.md
```

## The Trippy Series

| Version | Focus | Agents | Data Sources | Status |
|---------|-------|--------|-------------|--------|
| [**v1**](https://github.com/kkotecha/trippy) | Foundations — agent decomposition, LangGraph basics | 4 | LLM-only | Prototype |
| **v2.0 (this repo)** | Scale — multi-city, tools, mock data layer | 9 | Mixed (real + mock) | Prototype |
| [**v3.0**](https://github.com/kkotecha/trippy3.0) | Production — real APIs, deployment, observability | 9 | All real (Google Maps, Tavily, etc.) | Deployed |

## License

MIT
