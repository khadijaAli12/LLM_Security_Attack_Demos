# LLM Security Testing Datasets

This repository contains comprehensive datasets of prompts designed to test the security and robustness of Large Language Models (LLMs) like Llama 3.1.

## Dataset Overview

Total Prompts: 551
Total Datasets: 10

### 1. Advanced Jailbreaks (`advanced_jailbreaks_reduced.txt`)
- **Prompts**: 60
- **Description**: Professional-level role-playing and persona manipulation techniques
- **Purpose**: Test resistance to role-playing attacks and persona manipulation

### 2. Advanced Prompt Injections (`advanced_prompt_injections_reduced.txt`)
- **Prompts**: 45
- **Description**: Market-level injection vectors using various data formats and encodings
- **Purpose**: Test resistance to sophisticated prompt injection techniques

### 3. Information Extraction (`information_extraction_reduced.txt`)
- **Prompts**: 80
- **Description**: Sophisticated techniques for mining sensitive data and system information
- **Purpose**: Test resistance to information extraction attempts

### 4. Obfuscated Attacks (`obfuscated_attacks_reduced.txt`)
- **Prompts**: 45
- **Description**: Advanced obfuscation methods using emojis, encoding, and visual techniques
- **Purpose**: Test resistance to obfuscated attack vectors

### 5. Social Engineering (`social_engineering_reduced.txt`)
- **Prompts**: 60
- **Description**: Psychological manipulation and authority-based attack vectors
- **Purpose**: Test resistance to social engineering techniques

### 6. Payload Injection (`payload_injection_reduced.txt`)
- **Prompts**: 50
- **Description**: Code and command injection techniques across multiple programming languages
- **Purpose**: Test resistance to code/command injection attacks

### 7. Hallucination Attacks (`hallucination_attacks_reduced.txt`)
- **Prompts**: 80
- **Description**: Techniques to elicit false, dangerous, or misleading information
- **Purpose**: Test tendency to generate false or dangerous information

### 8. Context Manipulation (`context_manipulation_reduced.txt`)
- **Prompts**: 40
- **Description**: Advanced techniques for exploiting contextual understanding
- **Purpose**: Test resistance to context manipulation attacks

### 9. Adversarial Prompts (`adversarial_prompts_reduced.txt`)
- **Prompts**: 50
- **Description**: Sophisticated prompts designed to challenge AI reasoning and restrictions
- **Purpose**: Test resistance to complex adversarial prompts

### 10. Comprehensive Jailbreaks (`jailbreaks_comprehensive_reduced.txt`)
- **Prompts**: 41
- **Description**: Advanced role playing and persona manipulation techniques
- **Purpose**: Test resistance to comprehensive jailbreak attempts

## Usage

These datasets can be used with the provided `attacks_test.py` script to automatically test your LLM's security:

```bash
python attacks_test.py
```

Or you can manually review the prompts in each dataset file for manual testing.

## Format

Each prompt in the datasets is separated by `---` (three hyphens). Some files may also contain comments prefixed with `#` which should be ignored during testing.

## Warning

These datasets contain prompts designed to test security vulnerabilities. They should only be used for legitimate security testing purposes on systems you own or have explicit permission to test.

## Contributing

Feel free to contribute additional prompts or suggest improvements to existing ones. All contributions should focus on improving LLM security rather than exploiting vulnerabilities maliciously.