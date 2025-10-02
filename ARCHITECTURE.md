# Trip Planner Agent Architecture

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUT                                  │
│  destination: "Paris"                                               │
│  interests: ["museums", "food", "nightlife"]                        │
│  duration: 3 days                                                   │
│  budget: "moderate"                                                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INITIAL STATE CREATION                           │
│  {                                                                  │
│    destination: "Paris",                                            │
│    interests: ["museums", "food", "nightlife"],                    │
│    duration: 3,                                                     │
│    budget: "moderate",                                              │
│    itinerary: "",           ← Empty, will be filled                │
│    weather_info: "",        ← Empty, will be filled                │
│    local_tips: "",          ← Empty, will be filled                │
│    recommendations: {}      ← Empty, will be filled                │
│  }                                                                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   AGENT 1: RESEARCH DESTINATION                     │
│  Role: Travel Research Expert                                       │
│                                                                     │
│  Prompt: "Provide info about {destination}                          │
│           - Current season & weather                                │
│           - Best times to visit                                     │
│           - General travel tips                                     │
│           - Cultural considerations"                                │
│                                                                     │
│  LLM Call: OpenAI GPT-4-mini → Response                            │
│                                                                     │
│  State Update: weather_info = LLM response                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   AGENT 2: CREATE ITINERARY                         │
│  Role: Expert Travel Itinerary Planner                              │
│                                                                     │
│  Prompt: "Create {duration}-day itinerary for {destination}         │
│           User interests: {interests}                               │
│           Budget: {budget}                                          │
│           Weather context: {weather_info} ← From Agent 1            │
│                                                                     │
│           Provide:                                                  │
│           - Morning/afternoon/evening activities                    │
│           - Specific attractions                                    │
│           - Time estimates                                          │
│           - Meal suggestions                                        │
│           - Transportation tips"                                    │
│                                                                     │
│  LLM Call: OpenAI GPT-4-mini → Response                            │
│                                                                     │
│  State Update: itinerary = LLM response                             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   AGENT 3: GET LOCAL TIPS                           │
│  Role: Local Expert                                                 │
│                                                                     │
│  Prompt: "You are a local expert for {destination}                  │
│           Provide insider tips:                                     │
│           - Hidden gems                                             │
│           - Local restaurants                                       │
│           - Money-saving tips                                       │
│           - Safety considerations                                   │
│           - Local customs                                           │
│           - Transportation options                                  │
│           Budget: {budget}"                                         │
│                                                                     │
│  LLM Call: OpenAI GPT-4-mini → Response                            │
│                                                                     │
│  State Update: local_tips = LLM response                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   AGENT 4: COMPILE RECOMMENDATIONS                  │
│  Role: Data Compiler                                                │
│                                                                     │
│  Action: Package all collected information                          │
│                                                                     │
│  State Update:                                                      │
│    recommendations = {                                              │
│      weather_info: "..." ← From Agent 1                            │
│      itinerary: "..."    ← From Agent 2                            │
│      local_tips: "..."   ← From Agent 3                            │
│      interests: [...]                                               │
│      duration: 3                                                    │
│      budget: "moderate"                                             │
│    }                                                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FINAL RESPONSE                              │
│  {                                                                  │
│    destination: "Paris",                                            │
│    itinerary: "Full day-by-day plan...",                           │
│    recommendations: {                                               │
│      weather_info: "Current weather & best times...",              │
│      itinerary: "Full day-by-day plan...",                         │
│      local_tips: "Hidden gems & insider tips..."                   │
│    }                                                                │
│  }                                                                  │
│                                                                     │
│  Sent to Frontend → Displayed in tabs                              │
└─────────────────────────────────────────────────────────────────────┘
```

## LangGraph State Machine

```
     START
       │
       ▼
┌──────────────────┐
│ research_        │  State: destination, interests, duration, budget
│ destination      │  → Calls GPT-4 with research prompt
└────────┬─────────┘  → Updates: weather_info
         │
         │ (automatic transition)
         │
         ▼
┌──────────────────┐
│ create_          │  State: has weather_info from previous agent
│ itinerary        │  → Calls GPT-4 with itinerary prompt
└────────┬─────────┘  → Updates: itinerary
         │
         │ (automatic transition)
         │
         ▼
┌──────────────────┐
│ get_local_tips   │  State: has weather_info + itinerary
│                  │  → Calls GPT-4 with local expert prompt
└────────┬─────────┘  → Updates: local_tips
         │
         │ (automatic transition)
         │
         ▼
┌──────────────────┐
│ compile_         │  State: has all data
│ recommendations  │  → Packages everything into final structure
└────────┬─────────┘  → Updates: recommendations dict
         │
         ▼
       END
```

## Key Concepts

### 1. **State Management**
The `TripPlannerState` is a TypedDict that flows through all agents:

```python
{
    "messages": [],              # Conversation history
    "destination": "Paris",      # User input
    "interests": ["museums"],    # User input
    "duration": 3,               # User input
    "budget": "moderate",        # User input
    "itinerary": "",             # Filled by Agent 2
    "weather_info": "",          # Filled by Agent 1
    "local_tips": "",            # Filled by Agent 3
    "recommendations": {}        # Filled by Agent 4
}
```

Each agent:
1. Receives the current state
2. Processes it (calls LLM)
3. Returns updated state
4. LangGraph automatically passes to next agent

### 2. **Sequential Execution**
Agents execute in a fixed order (defined by edges):
- Agent 1 → Agent 2 → Agent 3 → Agent 4 → END

No branching or conditional logic (yet). Linear pipeline.

### 3. **Memory Persistence**
`MemorySaver()` keeps track of the state throughout execution, allowing you to:
- Resume interrupted workflows
- Track conversation history
- Debug intermediate states

### 4. **LLM Calls**
Each agent (except compiler) makes an independent LLM call with:
- **Different system prompts** (role specialization)
- **Access to previous state** (context awareness)
- **Specialized instructions** (task-specific)

## Data Flow Example

**Input:**
```json
{
  "destination": "Tokyo",
  "interests": ["anime", "food"],
  "duration": 5,
  "budget": "budget"
}
```

**After Agent 1 (Research):**
```json
{
  ...inputs,
  "weather_info": "Tokyo in September is mild with temperatures around 25°C..."
}
```

**After Agent 2 (Itinerary):**
```json
{
  ...inputs,
  "weather_info": "...",
  "itinerary": "Day 1: Morning - Visit Akihabara for anime culture..."
}
```

**After Agent 3 (Local Tips):**
```json
{
  ...inputs,
  "weather_info": "...",
  "itinerary": "...",
  "local_tips": "Hidden gem: Nakano Broadway for vintage anime..."
}
```

**After Agent 4 (Compile):**
```json
{
  ...inputs,
  "weather_info": "...",
  "itinerary": "...",
  "local_tips": "...",
  "recommendations": {
    "weather_info": "...",
    "itinerary": "...",
    "local_tips": "...",
    "interests": ["anime", "food"],
    "duration": 5,
    "budget": "budget"
  }
}
```

## Why LangGraph?

Traditional approach would require:
```python
weather = call_llm(research_prompt)
itinerary = call_llm(itinerary_prompt, weather)
tips = call_llm(tips_prompt)
return compile(weather, itinerary, tips)
```

LangGraph provides:
- ✅ **State management** - automatic state passing
- ✅ **Modularity** - easy to add/remove agents
- ✅ **Persistence** - save/resume workflows
- ✅ **Visibility** - track agent execution
- ✅ **Scalability** - add conditional logic, loops, human-in-the-loop
- ✅ **Type safety** - TypedDict ensures data consistency

## Future Enhancements

You could add:
- **Conditional routing** - Different paths based on budget/destination
- **Parallel execution** - Run multiple agents simultaneously
- **Human-in-the-loop** - Request user approval before continuing
- **Tool integration** - Add web search, weather APIs, booking systems
- **Error handling** - Retry failed agents
- **Cyclic workflows** - Allow agents to iterate/refine results