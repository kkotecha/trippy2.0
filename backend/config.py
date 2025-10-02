import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.5"))

# App
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Arize Phoenix
ARIZE_SPACE_ID = os.getenv("ARIZE_SPACE_ID")
ARIZE_API_KEY = os.getenv("ARIZE_API_KEY")
ARIZE_PROJECT_NAME = os.getenv("ARIZE_PROJECT_NAME", "trippy-multi-city")

# Validation
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY must be set in .env file")

print(f"✅ Config loaded: {OPENAI_MODEL}, Environment: {ENVIRONMENT}")
