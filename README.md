# Trippy 2.0 — Multi-City AI Trip Planner (Scale + Tool Abstraction)

A multi-city journey planner using **9 specialized LangGraph agents** with a **tool abstraction layer** that separates AI reasoning from data sources. Includes **Arize Phoenix Cloud** observability for tracing every agent, tool call, and LLM interaction across the entire pipeline.

**Part of a 3-project series:** See [Trippy v1](https://github.com/kkotecha/trippy) (foundations) and [Trippy 3.0](https://github.com/kkotecha/trippy3.0) (production with real APIs).

## Why This Version Exists

v1 proved that agent decomposition works. v2.0 tackles the next layer of AI product complexity:

- **Multi-agent scaling:** Going from 4 to 9 agents introduces coordination challenges — nested state, per-entity loops, and agent interdependencies
- **Tool-augmented agents:** LLM reasoning alone isn't enough. Agents need to call external tools (search, geocoding) and incorporate real-world data into their reasoning
- **Mock→Real migration:** How do you architect AI tools so you can iterate from prototype to production without rewriting agent logic?
- **Cloud observability:** Moving from local Phoenix to Arize Phoenix Cloud — persistent traces, team access, and the foundation for experiments and evaluations

The core question: **How do you design a multi-agent system where AI logic and data sources are cleanly separated, and every decision is observable?**

## What Changed from v1

| Aspect | v1 | v2.0 |
|--------|-----|------|
| Scope | Single city | 2-6 cities in one country |
| Agents | 4 (sequential) | 9 (sequential + per-city loop) |
| Tools | None (LLM-only) | 7 tools (2 real, 5 mock) |
| State | Flat TypedDict | Nested TypedDict with CityState sub-objects |
| Route Planning | N/A | TSP optimization with Geopy + OpenStreetMap |
| Observability | Phoenix local | **Arize Phoenix Cloud** |

## Architecture

### 9 Agents, 7 Tools

```
[User Input: country, cities, duration, interests, budget]
     │
     ▼
┌─────────────────────┐
│ 1. Country Research  │  ← Tavily web search (real tool)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 2. Route Planning    │  ← Geopy + OSM geocoding (real tool)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 3. Transport         │  ← Inter-city routes (mock tool)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 4-6. City Processing │  ← Per-city loop: hotels, itinerary, local transport
│      (per city)      │     (mock tools with real data shapes)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 7. Budget Compiler   │  ← Aggregates costs from all agents
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 8. Logistics         │  ← Packing, visas, currency (mock tools)
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ 9. Compiler          │  ← Final structured JSON
└────────┬────────────┘
         ▼
   [Complete Trip Plan]
```

### Tool Layer: Real vs Mock

| Tool | Source | Status |
|------|--------|--------|
| `web_search` | Tavily API | Real |
| `optimize_route` | Geopy + OSM | Real |
| `search_hotels` | Hardcoded mock | Mock |
| `search_trains` | 3 hardcoded routes | Mock |
| `search_attractions` | Generic mock | Mock |
| `get_visa_requirements` | 4 countries only | Mock |
| `get_currency_info` | 4 currencies only | Mock |

This is intentional. The mock tools define the **interface contract** — they return data in the exact shape that real APIs would. Swapping `search_hotels` from mock to Google Places API (done in v3.0) requires changing only the tool implementation. Agent logic, state management, and the graph remain untouched.

## AI & LLM Concepts

### LangGraph: Scaling Agent Orchestration

v2.0 introduces patterns that go beyond v1's linear pipeline:

**Per-entity loops:** The City Processing agents (4-6) run in a loop — once per city. The LangGraph graph handles this by iterating over `CityState` sub-objects within the main state. This is the pattern for any multi-entity AI workflow: per-customer analysis, per-document processing, per-product evaluation.

**Nested state management:** v1's flat `TypedDict` doesn't scale when you have per-city data. v2.0 introduces `CityState` as a sub-object — each city has its own hotels, itinerary, and transport data. The main `TripPlannerState` contains an array of `CityState` objects. This separation keeps state clean and agents focused.

**Tool-augmented reasoning:** Agents in v1 relied entirely on the LLM's knowledge. v2.0 agents call tools first (search, geocoding) and then reason over the results. The Country Research agent doesn't guess about Japan — it searches Tavily for current information and then synthesizes it. This is the fundamental RAG-adjacent pattern: **ground LLM reasoning in real data.**

### Tool Abstraction: The Product Architecture Decision

The most important architectural decision in v2.0 is the tool layer. Each tool is a `@tool`-decorated function with:
- A clear input/output contract
- A docstring that tells the LLM when and how to use it
- An implementation that can be swapped without changing the agent

**Why this matters for product:** When you're building an AI product, the question isn't "which API should we use?" — it's "what data shape does the agent need?" Design the interface first, implement with mocks, validate with real users, then swap in real APIs. This is how you avoid over-investing in API integrations before you've validated the product.

The `TOOL_IMPROVEMENT_ANALYSIS.md` in this repo documents the planned migration: which APIs to use, cost implications, and implementation priority for each mock tool. This is the kind of **product roadmap artifact** that bridges prototype to production.

### Arize Phoenix Cloud: Team-Level Observability

v2.0 moves from local Phoenix to **Arize Phoenix Cloud** — a significant shift:

**What changes:**
- Traces persist across sessions and deployments (not lost on restart)
- Team members can view traces without running the app locally
- Traces from different environments (dev, staging, production) are separated by project

**What Phoenix Cloud traces in this project:**
- All 9 agent executions with timing, token usage, and state snapshots
- Every tool call: which tool was invoked, what arguments were passed, what was returned
- LLM interactions: full prompts, responses, token counts, latency
- End-to-end request flow: from user input to final JSON output

**The PM perspective on cloud observability:**
Local Phoenix (v1) is great for development. But when you're evaluating whether your AI product is ready for users, you need persistent, shareable traces. Questions like "why did the Japan trip take 90 seconds?" or "why does the budget estimate look wrong for India?" require looking at specific traces — and sharing them with the team.

**What Phoenix Cloud enables beyond tracing:**
- **Experiments:** Compare two prompt variants for the Itinerary Agent across 50 saved inputs. Which produces better day-by-day plans? Phoenix runs both, side-by-side, with automated evaluation.
- **Evaluations:** Define quality criteria (e.g., "itinerary covers all user interests", "budget is within 20% of actual costs") and run automated checks on agent outputs.
- **Datasets:** Capture real trip requests as a test suite. Every time you change a prompt or model, run the suite and compare results.
- **A/B Testing foundation:** Route a percentage of traffic through a new agent configuration and compare quality metrics. This is how you iterate on AI products without regression.

## Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| Agent Orchestration | **LangGraph** + LangChain | 9-agent state machine with per-city loops |
| LLM | **OpenAI GPT-4o-mini** | Language model for all agents |
| Real Tools | **Tavily** (search), **Geopy** (geocoding) | Grounding agents in real data |
| AI Observability | **Arize Phoenix Cloud** | Persistent tracing, cost attribution, team access |
| Backend | FastAPI + Uvicorn | API server |
| Frontend | HTML, Tailwind CSS, Vanilla JS | Multi-city planner UI |

## Key Concepts Explored

**1. Tool Abstraction as Product Strategy**
Each tool is a `@tool`-decorated function with a clear interface. Mock tools return hardcoded data in the exact format real APIs would return. This means swapping `search_hotels` from mock to Google Places API requires changing only the tool implementation — agents, state, and graph remain untouched. **Design your tool interfaces around the data shape your agents need, not the API you're calling.**

**2. Nested State for Multi-Entity Workflows**
v1's flat state doesn't scale to multi-city. v2.0 introduces `CityState` as a sub-object within `TripPlannerState`, with per-city hotels, itineraries, and transport. This pattern applies to any multi-entity AI workflow — per-customer, per-document, per-product.

**3. Route Optimization: Algorithmic + AI**
The route planner uses a TSP (Travelling Salesman Problem) approach with Geopy geocoding to minimize backtracking across cities. This demonstrates a key pattern: **not everything needs an LLM.** Combine AI reasoning with algorithmic computation where each excels.

**4. Cloud Observability as a Team Capability**
Moving from local Phoenix to Arize Cloud isn't just about persistence — it's about making AI behavior a shared, inspectable artifact. When the whole team can see what agents are doing, product decisions about AI quality become data-driven instead of anecdotal.

**5. Mock→Real Migration Path**
The `TOOL_IMPROVEMENT_ANALYSIS.md` documents exactly which APIs to use, cost implications, and implementation priority for each mock tool. This is the product roadmap for going from prototype to production — a pattern applicable to any AI product with external dependencies.

## Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API key (required)
- Tavily API key (optional, for web search)
- Arize Phoenix account (optional, for cloud observability)

### Setup

```bash
git clone https://github.com/kkotecha/trippy2.0.git
cd trippy2.0/backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add: OPENAI_API_KEY (required)
# Add: TAVILY_API_KEY (optional, for web search)
# Add: ARIZE_SPACE_ID + ARIZE_API_KEY (optional, for Phoenix Cloud)

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

If you've explored v1 (or understand basic LangGraph), this repo teaches the next level — tool-augmented agents, multi-entity state, and cloud observability.

**Step 1: Compare agent architecture (v1 vs v2)**
v1 has all agents in one file. v2 splits them into `backend/agents/` (9 agents) and wires them together in `backend/graph/workflow.py`. Notice how the graph definition is separate from agent logic — this is the pattern for production agent systems.

**Step 2: Study the tool layer**
Open any file in `backend/tools/`. Notice how `search_hotels` returns structured data even as a mock. Now read `TOOL_IMPROVEMENT_ANALYSIS.md` to see the real API that would replace it. The interface stays the same. **This is the most reusable pattern in this repo** — applicable to any AI product with external data dependencies.

**Step 3: Trace a multi-city request in Phoenix Cloud**
Set up Arize credentials and plan a 3-city trip. Open the trace in Phoenix Cloud — you'll see all 9 agents, every tool call, and the per-city loop. Compare total token usage across agents. Which agent is most expensive? Which takes the longest? These are the questions a PM needs answered to prioritize optimization.

**Step 4: Inspect tool calls in traces**
In the Phoenix trace, find a tool call (e.g., `web_search`). See the arguments passed and the response returned. Now find a mock tool call (e.g., `search_hotels`). Compare the response shapes — they're identical in structure. This is the tool abstraction in action.

**Step 5: Swap a mock tool for a real one**
Pick `get_currency_info` (simplest) and replace the hardcoded data with a call to [ExchangeRate-API](https://www.exchangerate-api.com/) (free, no key needed). Run the same trip and check Phoenix — the agent behavior is unchanged, only the tool data is different.

**Then move to [Trippy 3.0](https://github.com/kkotecha/trippy3.0)** — where all tools are real, the system is deployed, and production concerns (cost management, parallel execution, deployment) are addressed.

## Project Structure

```
trippy2.0/
├── backend/
│   ├── main.py                        # FastAPI entry point
│   ├── config.py                      # Environment config
│   ├── observability.py               # Arize Phoenix Cloud setup
│   ├── agents/                        # 9 specialized LangGraph agents
│   │   ├── country_research.py        # Tavily search (real data)
│   │   ├── route_planning.py          # TSP route optimization
│   │   ├── transport.py               # Inter-city transport (mock)
│   │   ├── city_processing.py         # Per-city loop: hotels, attractions, local transport
│   │   ├── budget.py                  # Cost aggregation across all cities
│   │   ├── logistics.py               # Visa, currency, packing
│   │   └── compiler.py                # Final JSON builder
│   ├── tools/                         # Tool implementations (mock + real)
│   │   ├── search_tools.py            # web_search (Tavily - real)
│   │   ├── calculation_tools.py       # optimize_route (Geopy - real)
│   │   ├── hotel_tools.py             # search_hotels (mock → real in v3)
│   │   ├── transport_tools.py         # search_trains (mock → real in v3)
│   │   ├── attraction_tools.py        # search_attractions (mock → real in v3)
│   │   └── knowledge_tools.py         # visa/currency (mock → real in v3)
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

This series demonstrates the full lifecycle of building a multi-agent AI product — from first prototype to production deployment.

| Version | Focus | Agents | Data | Observability |
|---------|-------|--------|------|---------------|
| [**v1**](https://github.com/kkotecha/trippy) | Agent decomposition, LangGraph basics | 4 | LLM-only | Phoenix local |
| **v2.0 (this repo)** | Multi-city, tool abstraction, mock→real path | 9 | Mixed (2 real + 5 mock) | **Phoenix Cloud** |
| [**v3.0**](https://github.com/kkotecha/trippy3.0) | Production — real APIs, deployment, cost management | 9 | All real (Google Maps, Tavily, etc.) | Phoenix Cloud |

**The progression tells a product story:**
1. **v1**: Can specialized agents outperform a single prompt? (Yes — and Phoenix proves it.)
2. **v2.0**: Can we scale with a clean tool layer and make every agent decision observable?
3. **v3.0**: Can we ship it with real data and cost management that makes business sense?

## License

MIT
