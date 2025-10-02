"""
Observability configuration for both local Phoenix and Arize Cloud
"""
import os
from dotenv import load_dotenv

load_dotenv()

def setup_observability():
    """
    Set up observability based on environment variables:
    - If ARIZE_SPACE_ID and ARIZE_API_KEY are set: Use Arize AX Cloud
    - Otherwise: Use local Phoenix
    """
    arize_space_id = os.getenv("ARIZE_SPACE_ID")
    arize_api_key = os.getenv("ARIZE_API_KEY")
    arize_project_name = os.getenv("ARIZE_PROJECT_NAME", "trip-planner")

    if arize_space_id and arize_api_key:
        print("🌥️  Setting up Arize AX Cloud observability...")
        setup_arize_ax(arize_space_id, arize_api_key, arize_project_name)
    else:
        print("🔥 Setting up local Phoenix observability...")
        setup_local_phoenix()

def setup_local_phoenix():
    """Set up local Phoenix tracing"""
    import phoenix as px
    from phoenix.otel import register
    from openinference.instrumentation.langchain import LangChainInstrumentor

    # Launch Phoenix locally
    phoenix_session = px.launch_app()
    print(f"🔥 Phoenix UI available at: {phoenix_session.url}")

    # Initialize Phoenix tracing
    tracer_provider = register(
        project_name="trip-planner",
        endpoint="http://localhost:6006/v1/traces",
    )

    # Instrument LangChain
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

    return phoenix_session

def setup_arize_ax(space_id: str, api_key: str, project_name: str):
    """Set up Arize AX Cloud tracing using arize-otel"""
    from arize.otel import register
    from openinference.instrumentation.langchain import LangChainInstrumentor

    # Register with Arize AX
    tracer_provider = register(
        space_id=space_id,
        api_key=api_key,
        project_name=project_name,
    )

    # Instrument LangChain
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

    print("✅ Connected to Arize AX")
    print(f"📊 View traces at: https://app.arize.com/")
    print(f"🎯 Project: {project_name}")

    return tracer_provider