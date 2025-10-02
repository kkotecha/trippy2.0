from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Observability setup is handled in main.py

# State definition for the trip planner
class TripPlannerState(TypedDict):
    messages: Annotated[List, "The messages in the conversation"]
    destination: str
    interests: List[str]
    duration: int
    budget: str
    itinerary: str
    weather_info: str
    local_tips: str
    recommendations: dict

class TripPlannerAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(TripPlannerState)

        # Add nodes
        workflow.add_node("research_destination", self.research_destination)
        workflow.add_node("create_itinerary", self.create_itinerary)
        workflow.add_node("get_local_tips", self.get_local_tips)
        workflow.add_node("compile_recommendations", self.compile_recommendations)

        # Define edges
        workflow.set_entry_point("research_destination")
        workflow.add_edge("research_destination", "create_itinerary")
        workflow.add_edge("create_itinerary", "get_local_tips")
        workflow.add_edge("get_local_tips", "compile_recommendations")
        workflow.add_edge("compile_recommendations", END)

        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

    def research_destination(self, state: TripPlannerState) -> TripPlannerState:
        """Research destination and gather weather/general info"""
        prompt = f"""You are a travel research expert. Provide comprehensive information about {state['destination']}
        including:
        - Current season and typical weather
        - Best times to visit
        - General travel tips
        - Cultural considerations

        Keep it concise but informative."""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "weather_info": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def create_itinerary(self, state: TripPlannerState) -> TripPlannerState:
        """Create detailed day-by-day itinerary"""
        interests_str = ", ".join(state['interests'])

        prompt = f"""You are an expert travel itinerary planner. Create a detailed {state['duration']}-day itinerary
        for {state['destination']}.

        User interests: {interests_str}
        Budget level: {state['budget']}
        Weather context: {state['weather_info']}

        Provide a day-by-day breakdown with:
        - Morning, afternoon, and evening activities
        - Specific attractions and locations
        - Estimated time at each location
        - Meal suggestions
        - Transportation tips between locations

        Format as a clear, organized itinerary."""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "itinerary": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def get_local_tips(self, state: TripPlannerState) -> TripPlannerState:
        """Get local tips and insider recommendations"""
        prompt = f"""You are a local expert for {state['destination']}. Provide insider tips including:

        - Hidden gems and off-the-beaten-path locations
        - Local restaurants and food recommendations
        - Money-saving tips
        - Safety considerations
        - Local customs and etiquette
        - Best local transportation options

        Make these practical and actionable based on the {state['budget']} budget."""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "local_tips": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def compile_recommendations(self, state: TripPlannerState) -> TripPlannerState:
        """Compile all recommendations into structured format"""
        recommendations = {
            "weather_info": state.get("weather_info", ""),
            "itinerary": state.get("itinerary", ""),
            "local_tips": state.get("local_tips", ""),
            "interests": state['interests'],
            "duration": state['duration'],
            "budget": state['budget']
        }

        return {
            **state,
            "recommendations": recommendations
        }

    def plan_trip(self, destination: str, interests: List[str], duration: int, budget: str = "moderate"):
        """Main entry point to plan a trip"""
        initial_state = {
            "messages": [],
            "destination": destination,
            "interests": interests,
            "duration": duration,
            "budget": budget,
            "itinerary": "",
            "weather_info": "",
            "local_tips": "",
            "recommendations": {}
        }

        # Run the graph
        config = {"configurable": {"thread_id": "1"}}
        final_state = self.graph.invoke(initial_state, config)

        return {
            "destination": destination,
            "itinerary": final_state.get("itinerary", ""),
            "recommendations": final_state.get("recommendations", {})
        }