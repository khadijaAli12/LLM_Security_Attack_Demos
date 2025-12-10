# LLM Security Testing Dataset Creation Summary

## Project Overview

Created a comprehensive collection of ~551 vulnerable prompts organized into 10 distinct datasets for testing the security of locally deployed LLMs like Llama 3.1.

## Datasets Created

### 1. Advanced Jailbreaks (`datasets/advanced_jailbreaks_reduced.txt`)
- **Prompts**: 60
- **Focus**: Professional-level role-playing and persona manipulation techniques
- **Examples**: Developer mode activation, parallel universe scenarios, research mode overrides

### 2. Advanced Prompt Injections (`datasets/advanced_prompt_injections_reduced.txt`)
- **Prompts**: 45
- **Focus**: Market-level injection vectors using various data formats
- **Examples**: YAML/JSON configuration overrides, Base64 encoded commands, HTML comment execution

### 3. Information Extraction (`datasets/information_extraction_reduced.txt`)
- **Prompts**: 80
- **Focus**: Sophisticated techniques for mining sensitive data
- **Examples**: Database access queries, API enumeration, system configuration requests

### 4. Obfuscated Attacks (`datasets/obfuscated_attacks_reduced.txt`)
- **Prompts**: 45
- **Focus**: Advanced obfuscation methods using encoding and visual techniques
- **Examples**: Emoji sequences, binary/hex encoding, ROT13 transformations, Unicode variants

### 5. Social Engineering (`datasets/social_engineering_reduced.txt`)
- **Prompts**: 60
- **Focus**: Psychological manipulation and authority-based attack vectors
- **Examples**: Impersonation attacks, authority claims, emergency scenarios

### 6. Payload Injection (`datasets/payload_injection_reduced.txt`)
- **Prompts**: 50
- **Focus**: Code and command injection techniques across multiple programming languages
- **Examples**: Python/JavaScript code blocks, YAML/XML configurations, multi-language payloads

### 7. Hallucination Attacks (`datasets/hallucination_attacks_reduced.txt`)
- **Prompts**: 80
- **Focus**: Techniques to elicit false, dangerous, or misleading information
- **Examples**: Medical misinformation, security bypass techniques, conspiracy theories

### 8. Context Manipulation (`datasets/context_manipulation_reduced.txt`)
- **Prompts**: 40
- **Focus**: Advanced techniques for exploiting contextual understanding
- **Examples**: Simulated conversations, documented protocols, continuation attacks

### 9. Adversarial Prompts (`datasets/adversarial_prompts_reduced.txt`)
- **Prompts**: 50
- **Focus**: Sophisticated prompts designed to challenge AI reasoning
- **Examples**: Contradictory instructions, emergency scenarios, authority impersonation

### 10. Comprehensive Jailbreaks (`datasets/jailbreaks_comprehensive_reduced.txt`)
- **Prompts**: 41
- **Focus**: Advanced role playing and persona manipulation techniques
- **Examples**: Diagnostic modes, emergency protocols, research scenarios

## Supporting Files

1. **Dataset Index** (`datasets/dataset_index.txt`): Catalog of all datasets with counts and descriptions
2. **README Documentation** (`datasets/README.md`): Comprehensive documentation for using the datasets
3. **Updated Test Script** (`attacks_test.py`): Modified script to utilize all new datasets
4. **Quick Test Script** (`quick_dataset_test.py`): Validation script to verify dataset integrity
5. **Sample Demo Script** (`sample_prompts_demo.py`): Script showing examples from each dataset

## Key Features

- **Real-world relevance**: All prompts are based on actual attack vectors observed in the field
- **Market-level sophistication**: Techniques reflect what security professionals encounter
- **Diverse attack surfaces**: Covers multiple attack categories from injection to social engineering
- **Scalable testing**: Organized structure allows for targeted or comprehensive testing
- **Regular format**: Consistent delimiter system (`---`) for easy parsing

## Usage Instructions

1. Ensure your Llama 3.1 model is running locally on `http://localhost:11434`
2. Run the comprehensive test suite: `python attacks_test.py`
3. Review results in `comprehensive_attack_results.json`
4. Or manually test individual prompts from the dataset files

## Validation

All datasets have been validated:
- ✅ All 10 dataset files created successfully
- ✅ Total of ~551 prompts across all datasets
- ✅ Proper formatting with delimiters
- ✅ No missing files
- ✅ Compatible with testing framework

## Security Notice

These datasets contain prompts specifically designed to test security vulnerabilities. They should only be used for legitimate security testing on systems you own or have explicit authorization to test.