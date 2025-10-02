# AI Trip Planner with LangGraph

A full-stack trip planning application powered by LangGraph multi-agent system with a modern web frontend.

## Features

- **Multi-Agent Architecture**: Uses LangGraph to orchestrate multiple specialized agents:
  - Destination Research Agent
  - Itinerary Creation Agent
  - Local Tips & Insights Agent
  - Recommendations Compiler Agent

- **Interactive Frontend**: Clean, responsive UI for planning trips
- **Customizable Parameters**: Destination, interests, duration, and budget level
- **Comprehensive Output**: Day-by-day itinerary, weather info, and local insider tips

## Architecture

### Backend (LangGraph + FastAPI)
- **LangGraph Workflow**: State-based graph execution with memory
- **Multi-Agent System**: Specialized agents for different aspects of trip planning
- **REST API**: FastAPI endpoints for trip planning requests

### Frontend (Vanilla JS)
- Clean, responsive HTML/CSS/JS interface
- Tab-based results display
- Real-time API communication

## Setup Instructions

### Prerequisites
- Python 3.9+
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

5. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_actual_api_key_here
```

6. Run the backend server with Phoenix observability:
```bash
./run_with_phoenix.sh
```

Or manually:
```bash
python main.py
```

The following will be available:
- **Backend API**: `http://localhost:8000`
- **Phoenix UI**: `http://localhost:6006` (for observability and tracing)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Open `index.html` in a web browser, or use a simple HTTP server:
```bash
# Python 3
python -m http.server 3000

# Node.js (if you have http-server installed)
npx http-server -p 3000
```

3. Visit `http://localhost:3000` in your browser

## Usage

1. Enter your destination (e.g., "Paris", "Tokyo", "New York")
2. Add your interests as comma-separated values (e.g., "museums, food, nightlife")
3. Select trip duration (number of days)
4. Choose your budget level (Budget, Moderate, or Luxury)
5. Click "Plan My Trip"
6. View your personalized itinerary across three tabs:
   - **Itinerary**: Day-by-day breakdown of activities
   - **Weather & Tips**: Seasonal information and travel tips
   - **Local Insights**: Hidden gems and insider recommendations

## Project Structure

```
trippy/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── agent.py          # LangGraph agent implementation
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html        # Main HTML file
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
├── .env.example          # Environment variables template
└── README.md             # This file
```

## API Endpoints

### `GET /`
Health check endpoint

### `POST /plan-trip`
Plan a trip based on user inputs

**Request Body:**
```json
{
  "destination": "Paris",
  "interests": ["museums", "food", "architecture"],
  "duration": 5,
  "budget": "moderate"
}
```

**Response:**
```json
{
  "destination": "Paris",
  "itinerary": "Day 1: ...",
  "recommendations": {
    "weather_info": "...",
    "local_tips": "...",
    "interests": ["museums", "food", "architecture"],
    "duration": 5,
    "budget": "moderate"
  }
}
```

## LangGraph Workflow

The agent workflow follows this state machine:

```
[Start] → Research Destination → Create Itinerary → Get Local Tips → Compile Recommendations → [End]
```

Each node is a specialized agent that:
1. Takes the current state
2. Processes information using GPT-4
3. Updates the state with new information
4. Passes to the next node

## Technologies Used

- **Backend**: Python, FastAPI, LangGraph, LangChain, OpenAI GPT-4
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI Framework**: LangGraph for agent orchestration
- **Observability**: Arize Phoenix for tracing and monitoring

## Observability with Arize Phoenix

Phoenix provides real-time tracing and observability for your LangGraph agents:

### Features:
- 📊 **Trace Visualization**: See each agent's execution in real-time
- ⚡ **Performance Metrics**: Monitor LLM latency and token usage
- 🔍 **Debug Tools**: Inspect inputs/outputs for each agent step
- 📈 **Analytics**: Track usage patterns and costs

### Accessing Phoenix UI:

When you start the backend, Phoenix automatically launches at `http://localhost:6006`

You'll see:
1. **Traces**: Complete workflow execution from start to finish
2. **Agent Steps**: Each agent (Research, Itinerary, Local Tips, Compiler)
3. **LLM Calls**: OpenAI API calls with prompts and responses
4. **Timing**: Execution time for each step
5. **Token Usage**: Cost tracking for OpenAI API usage

### Phoenix Dashboard Features:

- **Projects View**: All trip planning sessions organized by project
- **Trace Details**: Click any trace to see the full agent workflow
- **Span Details**: Inspect individual agent executions
- **LLM Metrics**: Token counts, latency, model parameters
- **Error Tracking**: Catch and debug failed agent executions

## Future Enhancements

- Add real-time weather API integration
- Implement booking system integration
- Add user authentication and trip saving
- Include maps and visual itineraries
- Add more specialized agents (accommodation, dining, transportation)
- Implement streaming responses for real-time updates

## License

MIT