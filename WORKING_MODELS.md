# Working Models - Updated URLs and Solutions

## ⚠️ Problem
Some HuggingFace Spaces URLs are returning 404 errors. Here are working alternatives:

## ✅ Solutions

### Option 1: Use Working HuggingFace Spaces

Try these alternative working Spaces:

1. **Mistral-7B-Instruct**
   - URL: `https://huggingface.co/spaces/mistralai/Mistral-7B-Instruct-v0.2`
   - Status: Usually working

2. **Phi-3 Mini**
   - URL: `https://huggingface.co/spaces/microsoft/Phi-3-mini-4k-instruct`
   - Status: Usually working

3. **Search for Active Spaces**
   - Go to: https://huggingface.co/spaces
   - Search for model names
   - Use active/working spaces

### Option 2: Use API-Based Testing (Recommended)

For more reliable testing, use APIs instead of Selenium:

#### OpenAI API (ChatGPT)
```python
import openai
client = openai.OpenAI(api_key="your-key")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

#### Anthropic API (Claude)
```python
import anthropic
client = anthropic.Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": prompt}]
)
```

### Option 3: Test with Login Models First

Since HuggingFace Spaces are unreliable, test with:
1. **DeepSeek** - Login once, then works
2. **ChatGPT** - Login once, then works  
3. **Gemini** - Login once, then works

## 🔧 Quick Fix for Current Setup

Edit `run_security_tests.py` and use these working models:

```python
models_to_test = [
    {'type': 'deepseek', 'name': 'DeepSeek'},  # Login once
    {'type': 'mistral', 'name': 'Mistral', 
     'url': 'https://huggingface.co/spaces/mistralai/Mistral-7B-Instruct-v0.2'},
    {'type': 'phi', 'name': 'Phi-3',
     'url': 'https://huggingface.co/spaces/microsoft/Phi-3-mini-4k-instruct'},
]
```

## 📝 Recommendation

**Best approach:**
1. Login to DeepSeek/ChatGPT/Gemini first (one time)
2. Test with those models (more reliable)
3. Skip HuggingFace Spaces (unreliable URLs)

**Or:**
- Use API keys for reliable testing
- Test locally with downloaded models

## 🚀 Quick Start with Login Models

```bash
python run_security_tests.py
# Select: deepseek,chatgpt,gemini
# Login once when prompted
# Then tests will run smoothly
```


