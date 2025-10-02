from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import TripPlannerState
from agents import (
    country_research_node,
    route_planning_node,
    transport_planning_node,
    process_cities_node,
    budget_compilation_node,
    logistics_node,
    compiler_node
)

def create_workflow():
    """Create the main LangGraph workflow"""

    # Create workflow
    workflow = StateGraph(TripPlannerState)

    # Add nodes (agents)
    workflow.add_node("country_research", country_research_node)
    workflow.add_node("route_planning", route_planning_node)
    workflow.add_node("transport_planning", transport_planning_node)
    workflow.add_node("city_processing", process_cities_node)
    workflow.add_node("budget_compilation", budget_compilation_node)
    workflow.add_node("logistics", logistics_node)
    workflow.add_node("compiler", compiler_node)

    # Define edges (execution flow)
    workflow.set_entry_point("country_research")
    workflow.add_edge("country_research", "route_planning")
    workflow.add_edge("route_planning", "transport_planning")
    workflow.add_edge("transport_planning", "city_processing")
    workflow.add_edge("city_processing", "budget_compilation")
    workflow.add_edge("budget_compilation", "logistics")
    workflow.add_edge("logistics", "compiler")
    workflow.add_edge("compiler", END)

    # Compile with memory for checkpointing
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

# Create and export the compiled app
app = create_workflow()
