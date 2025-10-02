from typing import TypedDict, Annotated, List, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from operator import add

# Enhanced State definition with budget breakdown
class TripPlannerState(TypedDict):
    messages: Annotated[List, add]  # Use add operator to handle concurrent updates
    destination: str
    interests: List[str]
    duration: int
    budget: str
    itinerary: str
    weather_info: str
    local_tips: str
    budget_breakdown: str
    accommodation_suggestions: str
    transportation_info: str
    recommendations: dict

class ParallelTripPlannerAgent:
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
        """Build the LangGraph workflow - Sequential for now to avoid conflicts"""
        workflow = StateGraph(TripPlannerState)

        # Add all agent nodes
        workflow.add_node("research_destination", self.research_destination)
        workflow.add_node("budget_planning", self.budget_planning)
        workflow.add_node("create_itinerary", self.create_itinerary)
        workflow.add_node("accommodation_search", self.accommodation_search)
        workflow.add_node("transportation_planning", self.transportation_planning)
        workflow.add_node("get_local_tips", self.get_local_tips)
        workflow.add_node("compile_recommendations", self.compile_recommendations)

        # Sequential execution to avoid state conflicts
        workflow.set_entry_point("research_destination")
        workflow.add_edge("research_destination", "budget_planning")
        workflow.add_edge("budget_planning", "create_itinerary")
        workflow.add_edge("create_itinerary", "accommodation_search")
        workflow.add_edge("accommodation_search", "transportation_planning")
        workflow.add_edge("transportation_planning", "get_local_tips")
        workflow.add_edge("get_local_tips", "compile_recommendations")
        workflow.add_edge("compile_recommendations", END)

        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

    def research_destination(self, state: TripPlannerState) -> TripPlannerState:
        """Research destination and gather weather/general info"""
        prompt = f"""You are a travel research expert. Provide comprehensive information about {state['destination']}
        including:
        - Current season and typical weather for the time of year
        - Best times to visit
        - General travel tips
        - Cultural considerations
        - Safety information

        Keep it concise but informative."""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "weather_info": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def budget_planning(self, state: TripPlannerState) -> TripPlannerState:
        """Create detailed budget breakdown"""
        budget_levels = {
            "budget": "$50-100 per day",
            "moderate": "$150-300 per day",
            "luxury": "$500+ per day"
        }

        daily_budget = budget_levels.get(state['budget'], "$150-300 per day")

        prompt = f"""You are a travel budget expert. Create a detailed {state['duration']}-day budget breakdown
        for {state['destination']} with a {state['budget']} budget level ({daily_budget}).

        Provide a detailed breakdown including:
        - Accommodation costs (per night estimate)
        - Food & dining (breakfast, lunch, dinner estimates)
        - Transportation (local travel, metro passes, taxis)
        - Activities & attractions (based on interests: {', '.join(state['interests'])})
        - Miscellaneous (tips, souvenirs, emergencies)

        Format as:
        ## Total Budget: [amount]

        ### Daily Breakdown:
        - Accommodation: [amount]
        - Food: [amount]
        - Transportation: [amount]
        - Activities: [amount]
        - Miscellaneous: [amount]

        ### Tips for Saving Money:
        [practical tips]

        ### Budget Warnings:
        [things that might cost more than expected]"""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "budget_breakdown": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def create_itinerary(self, state: TripPlannerState) -> TripPlannerState:
        """Create detailed day-by-day itinerary"""
        interests_str = ", ".join(state['interests'])

        prompt = f"""You are an expert travel itinerary planner. Create a detailed {state['duration']}-day itinerary
        for {state['destination']}.

        User interests: {interests_str}
        Budget level: {state['budget']}
        Weather context: {state.get('weather_info', 'Not available')}
        Budget constraints: {state.get('budget_breakdown', 'Not available')}

        Provide a day-by-day breakdown with:
        - Morning, afternoon, and evening activities
        - Specific attractions and locations with addresses
        - Estimated time at each location
        - Meal suggestions (match budget level)
        - Transportation tips between locations
        - Estimated costs for each activity

        Format clearly by day (Day 1, Day 2, etc.)."""

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
        - Local restaurants and food recommendations (match {state['budget']} budget)
        - Money-saving tips specific to this location
        - Safety considerations and areas to avoid
        - Local customs, etiquette, and cultural norms
        - Best local transportation options
        - Apps and resources useful for tourists
        - Emergency contacts and important numbers

        Make these practical and actionable."""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "local_tips": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def accommodation_search(self, state: TripPlannerState) -> TripPlannerState:
        """Recommend accommodations based on budget"""
        prompt = f"""You are an accommodation specialist. Recommend places to stay in {state['destination']}
        for a {state['duration']}-day trip with a {state['budget']} budget.

        Provide:
        - 3-5 specific accommodation recommendations with:
          * Name and type (hotel, hostel, Airbnb, etc.)
          * Approximate location/neighborhood
          * Price range per night
          * Why it's a good fit for this budget
          * Booking tips

        - Neighborhood recommendations (where to stay vs where to avoid)
        - Best booking platforms/strategies
        - Tips for getting better deals

        Focus on value for money and location convenience."""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "accommodation_suggestions": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def transportation_planning(self, state: TripPlannerState) -> TripPlannerState:
        """Plan transportation options"""
        prompt = f"""You are a transportation expert for {state['destination']}.
        Plan transportation for a {state['duration']}-day trip with {state['budget']} budget.

        Provide:
        - Getting from airport to city center (options and costs)
        - Best local transportation methods (metro, bus, taxi, rideshare)
        - Transportation passes/cards worth buying
        - Average costs for different transport methods
        - Walking vs public transit vs rideshare analysis
        - Day trip transportation (if applicable)
        - Transportation apps to download
        - Tips for {state['budget']} budget travelers

        Be specific with routes, costs, and practical advice."""

        messages = [SystemMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return {
            **state,
            "transportation_info": response.content,
            "messages": state.get("messages", []) + [AIMessage(content=response.content)]
        }

    def compile_recommendations(self, state: TripPlannerState) -> TripPlannerState:
        """Compile all recommendations into structured format"""
        recommendations = {
            "weather_info": state.get("weather_info", ""),
            "budget_breakdown": state.get("budget_breakdown", ""),
            "itinerary": state.get("itinerary", ""),
            "local_tips": state.get("local_tips", ""),
            "accommodation": state.get("accommodation_suggestions", ""),
            "transportation": state.get("transportation_info", ""),
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
            "budget_breakdown": "",
            "accommodation_suggestions": "",
            "transportation_info": "",
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