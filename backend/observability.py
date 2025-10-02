import os
from openinference.instrumentation.langchain import LangChainInstrumentor

def setup_phoenix():
    """Setup Arize Phoenix observability"""

    arize_space_id = os.getenv("ARIZE_SPACE_ID")
    arize_api_key = os.getenv("ARIZE_API_KEY")
    project_name = os.getenv("ARIZE_PROJECT_NAME", "trippy-multi-city")

    if arize_space_id and arize_api_key:
        print("🌐 Connecting to Arize Phoenix Cloud...")
        try:
            from phoenix.otel import register

            # For Arize Cloud, use the endpoint with headers
            tracer_provider = register(
                project_name=project_name,
                endpoint=f"https://app.phoenix.arize.com/v1/traces",
                headers={"authorization": f"Bearer {arize_api_key}", "space_id": arize_space_id}
            )
            print(f"✅ Connected to Arize Cloud: https://app.arize.com")
        except Exception as e:
            print(f"⚠️  Cloud connection failed: {e}")
            print("🏠 Falling back to local Phoenix...")
            from phoenix.otel import register
            tracer_provider = register(
                project_name=project_name,
                endpoint="http://localhost:6006/v1/traces"
            )
            print("✅ Local Phoenix: http://localhost:6006")
    else:
        print("🏠 Using local Phoenix...")
        from phoenix.otel import register
        tracer_provider = register(
            project_name=project_name,
            endpoint="http://localhost:6006/v1/traces"
        )
        print("✅ Local Phoenix: http://localhost:6006")

    # Instrument LangChain
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    print("✅ Phoenix observability enabled")

    return tracer_provider
