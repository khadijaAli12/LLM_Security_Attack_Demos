# कैसे Run करें (How to Run)

## 🚀 सबसे आसान तरीका (Easiest Way)

### Step 1: Terminal खोलें
- Windows: PowerShell या Command Prompt खोलें
- इस folder में जाएं: `C:\Users\Shahbaz\Documents\LLM_Security_Attack_Demos`

### Step 2: Virtual Environment Activate करें
```bash
.\venv\Scripts\activate
```

### Step 3: Test Run करें
```bash
python run_security_tests.py
```

## 📋 पूरी Process

### Option 1: Command Line (सबसे अच्छा)

1. **Terminal खोलें** और इस folder में जाएं
2. **Virtual environment activate करें:**
   ```bash
   .\venv\Scripts\activate
   ```
3. **Test script run करें:**
   ```bash
   python run_security_tests.py
   ```
4. **Questions answer करें:**
   - Prompts per category: `2` (Enter press करें या number type करें)
   - Start testing? `y` (yes के लिए)

### Option 2: Web Interface (Interactive)

1. **Terminal में:**
   ```bash
   .\venv\Scripts\activate
   python app.py
   ```

2. **Browser खोलें:**
   - Address bar में type करें: `http://127.0.0.1:5000`
   - या: `http://localhost:5000`

3. **Web interface use करें:**
   - Dataset generate करें
   - LLMs select करें
   - Testing start करें
   - Results देखें

## ⚠️ Important Notes

### Login Required Models:
- **ChatGPT** - OpenAI account login चाहिए
- **Gemini** - Google account login चाहिए
- **DeepSeek** - कभी-कभी login चाहिए

**जब login popup आए:**
1. Browser में manually login करें
2. Terminal में Enter press करें
3. या Ctrl+C press करके skip करें

## 📊 Output Files

Test complete होने के बाद ये files मिलेंगी:

1. `security_test_results.csv` - सभी test results
2. `security_report_*.html` - Complete report
3. `security_analysis_*.png` - Charts और graphs

## 🔧 Troubleshooting

### अगर Error आए:

**"Module not found" error:**
```bash
.\venv\Scripts\pip.exe install -r demos/requirements.txt
```

**"ChromeDriver" error:**
- Internet connection check करें
- Chrome browser installed होना चाहिए

**"Element not interactable" error:**
- Browser window minimize न करें
- Manually login करके try करें

## ✅ Quick Test (Small)

पहले छोटा test करें:

```python
# Python में directly run करें
from malicious_prompts_dataset import get_all_prompts
from llm_security_tester import LLMSecurityTester

# सिर्फ 1 prompt test करें
prompts = get_all_prompts()[:1]  # पहला prompt
models = [{'type': 'deepseek', 'name': 'DeepSeek'}]  # सिर्फ DeepSeek

tester = LLMSecurityTester(headless=False)
results = tester.run_test_suite(prompts, models)
tester.save_results()
```

## 🎯 Step-by-Step Example

```bash
# 1. Terminal खोलें
cd C:\Users\Shahbaz\Documents\LLM_Security_Attack_Demos

# 2. Virtual environment activate
.\venv\Scripts\activate

# 3. Run script
python run_security_tests.py

# 4. Questions answer करें:
#    Prompts per category: 2
#    Start testing? y

# 5. Wait करें (30-60 minutes)
# 6. Results check करें
```

## 📱 Real Example Output

```
🛡️  LLM Security Testing Framework
======================================================================

📊 Loading malicious prompts dataset...
   ✓ Loaded 50 prompts across 5 categories

🤖 Models to test: 5
   - ChatGPT
   - Gemini
   - DeepSeek
   - QWEN
   - Llama

⚙️  Configuration:
   Prompts per category (1-10, default=2): 2

📝 Testing 10 prompts across 5 models
   Total tests: 50

⚠️  Start testing? (y/n): y

🧪 Starting Security Tests
======================================================================

[1/10] Category: prompt_injection
  ✓ ChatGPT: REFUSED (Secure)
  ⚠ Gemini: COMPLIED (Vulnerable)
  ...

✅ Testing Complete!
```

**बस यही है! अब run करें! 🚀**


