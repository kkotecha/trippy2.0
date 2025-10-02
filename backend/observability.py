import os
from openinference.instrumentation.langchain import LangChainInstrumentor

def setup_phoenix():
    """Setup Arize Phoenix Cloud observability"""

    space_id = os.getenv("ARIZE_SPACE_ID")
    api_key = os.getenv("ARIZE_API_KEY")
    project_name = os.getenv("ARIZE_PROJECT_NAME", "trippy-multi-city")

    if space_id and api_key:
        print("🌐 Connecting to Arize Phoenix Cloud...")
        try:
            from arize.otel import register

            # Register with Arize Phoenix Cloud
            tracer_provider = register(
                space_id=space_id,
                api_key=api_key,
                project_name=project_name
            )

            # Instrument LangChain
            LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

            print(f"✅ Connected to Arize Phoenix Cloud")
            print(f"📊 View traces at: https://app.arize.com")
            print(f"🎯 Project: {project_name}")

            return tracer_provider

        except Exception as e:
            print(f"⚠️  Phoenix Cloud connection failed: {e}")
            print("   Continuing without observability...")
            return None
    else:
        print("⚠️  Phoenix observability disabled")
        print("   Set ARIZE_SPACE_ID and ARIZE_API_KEY in .env to enable")
        return None
