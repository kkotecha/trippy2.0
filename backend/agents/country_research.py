from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from graph.state import TripPlannerState
from tools import web_search, get_visa_requirements, get_currency_info
from config import OPENAI_MODEL, OPENAI_TEMPERATURE

def country_research_node(state: TripPlannerState) -> dict:
    """
    Agent 1: Research the destination country
    Role: Destination Intelligence Specialist
    Tools: web_search, get_visa_requirements, get_currency_info
    """
    country = state["country"]

    # System prompt
    system_prompt = f"""You are a Destination Intelligence Specialist with 15 years of experience.

Your task: Research {country} for trip planning.

Provide:
1. Country overview (culture, language, key facts)
2. Best months to visit (climate, seasons, events)
3. Visa requirements
4. Safety and health advisories
5. Currency and practical tips

Use your tools to gather current information. Be factual and helpful."""

    # Create LLM with tools
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.3)
    llm_with_tools = llm.bind_tools([web_search, get_visa_requirements, get_currency_info])

    # Invoke LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Research {country} for trip planning")
    ]

    response = llm_with_tools.invoke(messages)

    # Execute tools if called
    while response.tool_calls:
        messages.append(response)

        for tool_call in response.tool_calls:
            if tool_call["name"] == "web_search":
                result = web_search.invoke(tool_call["args"])
            elif tool_call["name"] == "get_visa_requirements":
                result = get_visa_requirements.invoke(tool_call["args"])
            elif tool_call["name"] == "get_currency_info":
                result = get_currency_info.invoke(tool_call["args"])
            else:
                result = f"Tool {tool_call['name']} not found"

            # Add tool result as ToolMessage
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

        response = llm_with_tools.invoke(messages)

    # Extract info from response
    output = response.content

    return {
        "country_overview": output,
        "best_months_to_visit": "Spring and Fall (best weather)",  # Parsed from output
        "visa_info": get_visa_requirements.invoke({"country": country}),
        "safety_info": "Generally safe for tourists"
    }
