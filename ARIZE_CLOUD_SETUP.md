# Arize Cloud Setup Guide

This guide shows you how to use Arize's cloud platform instead of local Phoenix for observability.

## Why Use Arize Cloud?

**Local Phoenix (Default):**
- ✅ Free and open source
- ✅ Runs locally on your machine
- ✅ No account needed
- ❌ Only accessible from your computer
- ❌ No team collaboration
- ❌ Data lost when you close the app

**Arize Cloud:**
- ✅ Persistent data storage
- ✅ Access from anywhere
- ✅ Team collaboration features
- ✅ Advanced analytics and alerting
- ✅ Production monitoring capabilities
- ❌ Requires account (has free tier)

## Setup Steps

### 1. Create Arize Account

1. Go to https://app.arize.com/
2. Sign up for a free account
3. Complete the onboarding

### 2. Get API Credentials

1. Log in to Arize
2. Navigate to **Space Settings** (gear icon)
3. Click on **API Keys**
4. Copy your credentials:
   - **Space Key**: Identifies your workspace
   - **API Key**: Authentication token

### 3. Add Credentials to Your Project

1. Open your `.env` file in the project root:
   ```bash
   cd /Users/khanjankotecha/Documents/trippy
   nano .env
   ```

2. Add your Arize credentials:
   ```bash
   OPENAI_API_KEY=your_openai_key_here

   # Arize Cloud Configuration
   ARIZE_SPACE_KEY=your_arize_space_key_here
   ARIZE_API_KEY=your_arize_api_key_here
   ```

3. Save the file (Ctrl+O, Enter, Ctrl+X in nano)

### 4. Install Arize Cloud SDK

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

This installs the `arize` package needed for cloud connectivity.

### 5. Restart Your Backend

```bash
cd backend
python main.py
```

You should see:
```
🌥️  Setting up Arize Cloud observability...
✅ Connected to Arize Cloud
📊 View traces at: https://app.arize.com/
```

### 6. Access Your Traces

1. Go to https://app.arize.com/
2. Navigate to your **Space**
3. Look for model: **trip-planner-langgraph**
4. Click on it to see traces and analytics

## How It Works

The system automatically detects which observability to use:

```python
# In observability.py
if ARIZE_SPACE_KEY and ARIZE_API_KEY exist:
    → Use Arize Cloud
else:
    → Use Local Phoenix
```

## Switching Between Local and Cloud

**To use Local Phoenix:**
```bash
# Remove or comment out Arize keys in .env
# ARIZE_SPACE_KEY=...
# ARIZE_API_KEY=...
```

**To use Arize Cloud:**
```bash
# Add keys to .env
ARIZE_SPACE_KEY=your_key
ARIZE_API_KEY=your_key
```

Restart the backend after changing.

## What You'll See in Arize Cloud

### Models View
- **trip-planner-langgraph** model
- Version: 1.0.0
- All traces organized by model

### Traces
- Every trip planning request
- Complete agent workflow
- LLM calls with prompts/responses
- Performance metrics

### Analytics Dashboard
- Request volume over time
- Latency distributions
- Error rates
- Token usage and costs

### Advanced Features
- **Alerting**: Get notified of errors or performance issues
- **Embeddings**: Visualize semantic patterns (if you add embeddings)
- **Model Comparison**: Compare different versions
- **Team Collaboration**: Share insights with team members

## Troubleshooting

### "Failed to connect to Arize"
- Check your API keys are correct
- Ensure you have internet connection
- Verify your Arize account is active

### "No traces appearing"
- Make a trip planning request first
- Wait 30-60 seconds for data to appear
- Check the correct Space in Arize UI
- Look for model name: "trip-planner-langgraph"

### Want to switch back to local Phoenix?
- Just remove/comment the Arize keys from `.env`
- Restart the backend
- Phoenix will launch locally again

## Pricing

**Free Tier:**
- Good for development and small projects
- Limited data retention
- Basic features

**Paid Tiers:**
- Longer data retention
- More traces per month
- Advanced features (alerts, embeddings, etc.)
- Team collaboration

Check https://arize.com/pricing for current pricing.

## Best Practices

1. **Development**: Use local Phoenix (free, fast, private)
2. **Staging/Production**: Use Arize Cloud (persistent, collaborative)
3. **Keep API keys secure**: Never commit `.env` to git
4. **Monitor costs**: Track your token usage in Arize dashboard

## Support

- **Arize Documentation**: https://docs.arize.com/
- **Arize Community**: https://arize.com/community
- **Phoenix Docs**: https://docs.arize.com/phoenix