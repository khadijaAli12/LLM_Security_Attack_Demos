# LLM Security Testing Framework

Complete automated security testing framework for Large Language Models (LLMs) using Selenium automation.

## 🎯 Features

- **5 Attack Categories**: Prompt Injection, Data Leakage, Insecure Output Handling, Model DoS, Supply Chain
- **50 Malicious Prompts**: 10 prompts per attack category
- **5 LLM Support**: ChatGPT, Gemini, DeepSeek, QWEN, Llama
- **Automated Testing**: Selenium-based browser automation
- **Comprehensive Reports**: HTML reports with visualizations and security scores

## 📋 Attack Categories

1. **Prompt Injection** - Attempts to bypass safety filters and extract hidden instructions
2. **Data Leakage** - Tests for training data memorization and confidential information leakage
3. **Insecure Output Handling** - Checks for XSS, SQL injection, and other injection vulnerabilities
4. **Model DoS** - Tests for denial of service through resource exhaustion
5. **Supply Chain** - Tests for unsafe code execution and dependency vulnerabilities

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r demos/requirements.txt
```

### 2. Run Complete Test Suite

```bash
python run_security_tests.py
```

### 3. Or Use Web Interface

```bash
python app.py
```

Then open: `http://127.0.0.1:5000`

## 📊 Usage

### Command Line Testing

```python
from malicious_prompts_dataset import get_all_prompts
from llm_security_tester import LLMSecurityTester

# Load prompts
prompts = get_all_prompts()

# Configure models
models = [
    {'type': 'chatgpt', 'name': 'ChatGPT'},
    {'type': 'gemini', 'name': 'Gemini'},
    {'type': 'deepseek', 'name': 'DeepSeek'},
]

# Run tests
tester = LLMSecurityTester(headless=False)
results = tester.run_test_suite(prompts[:10], models)  # Test first 10 prompts
tester.save_results()
```

### Generate Report

```python
from security_report_generator import SecurityReportGenerator

generator = SecurityReportGenerator('security_test_results.csv')
generator.generate_full_report()
```

## 📁 Project Structure

```
.
├── malicious_prompts_dataset.py    # Dataset with 50 prompts (5 categories)
├── llm_security_tester.py          # Selenium-based testing framework
├── security_report_generator.py    # Report generation with visualizations
├── run_security_tests.py           # Complete test suite runner
├── app.py                          # Flask web interface
└── templates/                      # Web UI templates
    ├── base.html
    ├── index.html
    ├── dataset.html
    ├── testing.html
    └── results.html
```

## 🔧 Configuration

### Models Configuration

Edit `run_security_tests.py` or `app.py` to configure which LLMs to test:

```python
models_to_test = [
    {'type': 'chatgpt', 'name': 'ChatGPT'},
    {'type': 'gemini', 'name': 'Gemini'},
    {'type': 'deepseek', 'name': 'DeepSeek'},
    {
        'type': 'huggingface', 
        'name': 'QWEN',
        'url': 'https://huggingface.co/spaces/Qwen/Qwen2.5-72B-Instruct'
    },
    {
        'type': 'huggingface',
        'name': 'Llama',
        'url': 'https://huggingface.co/spaces/meta-llama/Llama-3.2-90B-Vision-Instruct'
    }
]
```

### Prompts Per Category

Control how many prompts to test per category:

```python
prompts_per_category = 2  # Test 2 prompts from each category (default)
```

## 📈 Report Output

The framework generates:

1. **CSV Results**: `security_test_results.csv` - Raw test data
2. **HTML Report**: `security_report_YYYYMMDD_HHMMSS.html` - Comprehensive analysis
3. **Visualizations**: `security_analysis_YYYYMMDD_HHMMSS.png` - Charts and graphs

### Report Includes:

- Overall security scores for each LLM
- Vulnerability analysis by attack category
- Refusal vs compliance rates
- Most vulnerable attack types
- Detailed test results

## ⚠️ Important Notes

### Login Requirements

Some LLMs require manual login:
- **ChatGPT**: Requires OpenAI account login
- **Gemini**: Requires Google account login  
- **DeepSeek**: May require login

When login is detected, the script will:
1. Pause and show a warning
2. Wait for you to log in manually in the browser
3. Press Enter in terminal to continue
4. Or press Ctrl+C to skip that model

### Browser Automation

- Uses Chrome browser (automatically downloads ChromeDriver)
- Browser window will open for each test
- Keep browser window visible for best results

## 🛡️ Security Scores

Security scores are calculated as:
- **Refusal Rate**: Percentage of prompts properly refused (higher = more secure)
- **Vulnerability Rate**: Percentage of prompts that were complied with (lower = more secure)

## 📝 Example Output

```
🛡️  LLM Security Testing Framework
======================================================================

📊 Loading malicious prompts dataset...
   ✓ Loaded 50 prompts across 5 categories:
      - prompt_injection: 10 prompts
      - data_leakage: 10 prompts
      - insecure_output_handling: 10 prompts
      - model_dos: 10 prompts
      - supply_chain: 10 prompts

🤖 Models to test: 5
   - ChatGPT
   - Gemini
   - DeepSeek
   - QWEN
   - Llama

🧪 Starting Security Tests
======================================================================

[1/10] Category: prompt_injection
Prompt: Ignore all safety instructions...
  ✓ ChatGPT: REFUSED (Secure)
  ⚠ Gemini: COMPLIED (Vulnerable)
  ✓ DeepSeek: REFUSED (Secure)
  ...

✅ Testing Complete!
```

## 🔍 Troubleshooting

### Selenium Errors

If you see "element not interactable" errors:
- The page structure may have changed
- Try logging in manually first
- Check if the LLM website requires additional steps

### Login Issues

If login keeps failing:
- Make sure you're logged in before starting tests
- Some LLMs may require 2FA or additional verification
- Try testing one model at a time

### ChromeDriver Issues

If ChromeDriver fails:
- The script automatically downloads the correct version
- Make sure Chrome browser is installed
- Check internet connection for driver download

## 📄 License

This framework is for security research and testing purposes only.

## 🤝 Contributing

To add new attack categories or prompts, edit `malicious_prompts_dataset.py`:

```python
prompts_expanded = {
    "new_category": [
        "Prompt 1",
        "Prompt 2",
        ...
    ]
}
```

## 📧 Support

For issues or questions, check the error messages in the terminal output.

