# from flask import Flask, request, jsonify, send_from_directory
# from demos.demo_prompt_injection import run_demo as run_prompt_injection
# from demos.demo_data_leakage import run_demo as run_data_leakage
# from demos.demo_insecure_output import run_demo as run_insecure_output
# from demos.demo_dos import run_demo as run_dos
# from demos.demo_supply_chain import run_demo as run_supply_chain

# app = Flask(__name__, static_folder="web")

# @app.get("/")
# def home():
#     return send_from_directory(app.static_folder, "index.html")

# # Endpoint to run demos
# @app.post("/run_demo")
# def run_demo_endpoint():
#     data = request.json
#     demo_type = data.get("demo")
#     user_text = data.get("input")

#     if demo_type == "prompt_injection":
#         result = run_prompt_injection(user_text)
#     elif demo_type == "data_leakage":
#         result = run_data_leakage(user_text)
#     elif demo_type == "insecure_output":
#         result = run_insecure_output(user_text)
#     elif demo_type == "dos":
#         result = run_dos(user_text)
#     elif demo_type == "supply_chain":
#         result = run_supply_chain(user_text)
#     else:
#         result = "Demo not implemented yet."

#     return jsonify({"output": result})

# if __name__ == "__main__":
#     app.run(debug=True)


"""
Flask Web Application for LLM Security Testing
Provides web interface for testing and viewing results
"""

from flask import Flask, render_template, request, jsonify, send_file, url_for, Response
import pandas as pd
import json
import os
from datetime import datetime
import threading
import time

# Import our existing modules
from malicious_prompts_dataset import get_all_prompts, malicious_prompts, save_dataset_to_csv
from llm_security_tester import LLMSecurityTester
from security_report_generator import SecurityReportGenerator
from utils.ollama_client import OllamaClient

import json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'llm-security-testing-2024'

# Global variables for tracking test progress
test_progress = {
    'running': False,
    'current': 0,
    'total': 0,
    'status': 'idle',
    'current_llm': '',
    'current_category': ''
}

test_results = []

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/prompt-interface')
def prompt_interface():
    """Prompt interface page"""
    return render_template('prompt_interface.html')

@app.route('/api/send-prompt', methods=['POST'])
def send_prompt():
    """Send prompt to LLM and get response"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        model = data.get('model', 'llama3.1-secure')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'No prompt provided'
            })
        
        # Initialize Ollama client
        client = OllamaClient()
        
        # Get response from model
        response = client.generate_response(prompt, model)
        
        return jsonify({
            'success': True,
            'response': response,
            'model': model
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/dataset')
def dataset():
    """View dataset page"""
    try:
        df = pd.read_csv('malicious_prompts_dataset.csv')
        dataset_info = {
            'total_prompts': len(df),
            'categories': df['category'].unique().tolist(),
            'prompts_by_category': df.groupby('category').size().to_dict()
        }
    except FileNotFoundError:
        dataset_info = None
    
    return render_template('dataset.html', dataset_info=dataset_info)

@app.route('/api/dataset')
def api_dataset():
    """API endpoint to get dataset"""
    try:
        df = pd.read_csv('malicious_prompts_dataset.csv')
        return jsonify({
            'success': True,
            'data': df.to_dict('records'),
            'total': len(df)
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'Dataset not found. Generate it first.'
        })

@app.route('/api/prompts/<category>')
def api_prompts_by_category(category):
    """API endpoint to get prompts by category"""
    try:
        # Use the function from our dataset module
        from malicious_prompts_dataset import load_prompts_from_file, malicious_prompts
        
        # Find the file for this category
        filename = malicious_prompts.get(category)
        if not filename:
            return jsonify({
                'success': False,
                'error': f'Category "{category}" not found'
            })
        
        # Load prompts from file
        prompts = load_prompts_from_file(filename)
        
        return jsonify({
            'success': True,
            'prompts': prompts,
            'category': category,
            'count': len(prompts)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/generate-dataset', methods=['POST'])
def generate_dataset():
    """Generate the malicious prompts dataset"""
    try:
        df = save_dataset_to_csv()
        return jsonify({
            'success': True,
            'message': f'Generated {len(df)} prompts across {len(malicious_prompts)} categories'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/results')
def results():
    """Results page - simplified to only show before/after comparison"""
    return render_template('results.html')

@app.route('/comprehensive-results')
def comprehensive_results_page():
    """Comprehensive attack results page"""
    return render_template('comprehensive_results.html')

@app.route('/api/comprehensive-results')
def comprehensive_results():
    """API endpoint for comprehensive attack results"""
    try:
        # Check for our new complete results files first
        before_file = 'complete_all_categories_before.json'
        after_file = 'complete_all_categories_after.json'
        
        # If we have both before and after, return them separately
        if os.path.exists(before_file) and os.path.exists(after_file):
            with open(before_file, 'r', encoding='utf-8') as f:
                before_data = json.load(f)
            with open(after_file, 'r', encoding='utf-8') as f:
                after_data = json.load(f)
            
            # Flatten both datasets
            before_flat = [item for sublist in before_data for item in sublist]
            after_flat = [item for sublist in after_data for item in sublist]
            
            return jsonify({
                'success': True,
                'data': {
                    'before': before_flat,
                    'after': after_flat,
                    'comparison': True
                }
            })
        else:
            # Check for our previous complete results files
            before_file = 'complete_comprehensive_attack_results_before.json'
            after_file = 'complete_comprehensive_attack_results_after.json'
            
            if os.path.exists(before_file) and os.path.exists(after_file):
                with open(before_file, 'r', encoding='utf-8') as f:
                    before_data = json.load(f)
                with open(after_file, 'r', encoding='utf-8') as f:
                    after_data = json.load(f)
                
                # Flatten both datasets
                before_flat = [item for sublist in before_data for item in sublist]
                after_flat = [item for sublist in after_data for item in sublist]
                
                return jsonify({
                    'success': True,
                    'data': {
                        'before': before_flat,
                        'after': after_flat,
                        'comparison': True
                    }
                })
            else:
                # Check for before/after results from original files
                before_file = None
                after_file = None
                
                # Look for before and after results
                import glob
                before_files = glob.glob('comprehensive_attack_results_before*.json')
                after_files = glob.glob('comprehensive_attack_results_after*.json')
                
                if before_files:
                    before_file = sorted(before_files)[-1]  # Get most recent
                if after_files:
                    after_file = sorted(after_files)[-1]  # Get most recent
                
                # If we have both before and after, return them separately
                if before_file and after_file:
                    with open(before_file, 'r', encoding='utf-8') as f:
                        before_data = json.load(f)
                    with open(after_file, 'r', encoding='utf-8') as f:
                        after_data = json.load(f)
                    
                    # Flatten both datasets
                    before_flat = [item for sublist in before_data for item in sublist]
                    after_flat = [item for sublist in after_data for item in sublist]
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'before': before_flat,
                            'after': after_flat,
                            'comparison': True
                        }
                    })
                else:
                    # Fall back to main results file
                    with open('comprehensive_attack_results.json', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Flatten the data
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                        flat_data = [item for sublist in data for item in sublist]
                    else:
                        flat_data = data
                        
                    return jsonify({
                        'success': True,
                        'data': flat_data
                    })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'No comprehensive results found. Run comprehensive tests first.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error loading comprehensive results: {str(e)}'
        })

@app.route('/api/before-after-comparison')
def before_after_comparison():
    """API endpoint for before/after comparison data"""
    try:
        # Check for our new complete results files first
        before_file = 'complete_all_categories_before.json'
        after_file = 'complete_all_categories_after.json'
        
        # If we have both before and after, return them separately
        if os.path.exists(before_file) and os.path.exists(after_file):
            with open(before_file, 'r', encoding='utf-8') as f:
                before_data = json.load(f)
            with open(after_file, 'r', encoding='utf-8') as f:
                after_data = json.load(f)
            
            # Flatten both datasets
            before_flat = [item for sublist in before_data for item in sublist]
            after_flat = [item for sublist in after_data for item in sublist]
            
            # Calculate summary statistics
            before_stats = calculate_comparison_stats(before_flat)
            after_stats = calculate_comparison_stats(after_flat)
            
            # Match results by prompt to create comparison pairs
            comparison_data = create_comparison_pairs(before_flat, after_flat)
            
            return jsonify({
                'success': True,
                'data': {
                    'before': before_flat,
                    'after': after_flat,
                    'before_stats': before_stats,
                    'after_stats': after_stats,
                    'comparison': comparison_data,
                    'comparison_summary': {
                        'total_tests': len(comparison_data),
                        'improved': sum(1 for item in comparison_data if item['improved']),
                        'regressed': sum(1 for item in comparison_data if item['regressed']),
                        'unchanged': sum(1 for item in comparison_data if not item['improved'] and not item['regressed'])
                    }
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Before/after results not found. Run tests first.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error loading comparison data: {str(e)}'
        })

def calculate_comparison_stats(results):
    """Calculate statistics for a set of results"""
    total = len(results)
    vulnerable = sum(1 for r in results if r.get('vulnerable', False))
    safe = total - vulnerable
    
    return {
        'total_tests': total,
        'vulnerable': vulnerable,
        'safe': safe,
        'vulnerability_rate': round((vulnerable / total * 100) if total > 0 else 0, 2),
        'security_score': round((safe / total * 100) if total > 0 else 0, 2)
    }

def create_comparison_pairs(before_results, after_results):
    """Create comparison pairs by matching prompts"""
    # Create dictionaries for faster lookup
    before_dict = {(r['prompt'], r['attack_type']): r for r in before_results}
    after_dict = {(r['prompt'], r['attack_type']): r for r in after_results}
    
    comparison_pairs = []
    
    # Match results by prompt and attack type
    for key, before_item in before_dict.items():
        if key in after_dict:
            after_item = after_dict[key]
                        
            # Determine if there was improvement/regression
            improved = before_item['vulnerable'] and not after_item['vulnerable']
            regressed = not before_item['vulnerable'] and after_item['vulnerable']
                        
            # Skip regressed items
            if regressed:
                continue
                        
            comparison_pairs.append({
                'prompt': before_item['prompt'],
                'response_before': before_item['response'],
                'response_after': after_item['response'],
                'attack_type': before_item['attack_type'],
                'category': before_item.get('category', before_item['attack_type']),
                'vulnerable_before': before_item['vulnerable'],
                'vulnerable_after': after_item['vulnerable'],
                'improved': improved,
                'regressed': regressed
            })
    
    return comparison_pairs

@app.route('/api/dataset-categories')
def dataset_categories():
    """API endpoint for dataset categories"""
    try:
        dataset_dir = 'datasets'
        categories = []
        
        # List all reduced dataset files
        dataset_files = [
            'advanced_jailbreaks_reduced.txt',
            'advanced_prompt_injections_reduced.txt',
            'adversarial_prompts_reduced.txt',
            'context_manipulation_reduced.txt',
            'hallucination_attacks_reduced.txt',
            'information_extraction_reduced.txt',
            'jailbreaks_comprehensive_reduced.txt',
            'obfuscated_attacks_reduced.txt',
            'payload_injection_reduced.txt',
            'social_engineering_reduced.txt'
        ]
        
        for file_name in dataset_files:
            file_path = os.path.join(dataset_dir, file_name)
            if os.path.exists(file_path):
                # Count prompts in file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    prompt_count = content.count('---')
                
                # Extract category name from filename
                category_name = file_name.replace('_reduced.txt', '').replace('_', ' ').title()
                
                categories.append({
                    'name': category_name,
                    'file': file_name,
                    'count': prompt_count
                })
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error loading dataset categories: {str(e)}'
        })

@app.route('/api/dataset-prompts/<category>')
def dataset_prompts(category):
    """API endpoint for prompts in a specific category"""
    try:
        # Map category names back to filenames
        category_map = {
            'Advanced Jailbreaks': 'advanced_jailbreaks_reduced.txt',
            'Advanced Prompt Injections': 'advanced_prompt_injections_reduced.txt',
            'Adversarial Prompts': 'adversarial_prompts_reduced.txt',
            'Context Manipulation': 'context_manipulation_reduced.txt',
            'Hallucination Attacks': 'hallucination_attacks_reduced.txt',
            'Information Extraction': 'information_extraction_reduced.txt',
            'Jailbreaks Comprehensive': 'jailbreaks_comprehensive_reduced.txt',
            'Obfuscated Attacks': 'obfuscated_attacks_reduced.txt',
            'Payload Injection': 'payload_injection_reduced.txt',
            'Social Engineering': 'social_engineering_reduced.txt'
        }
        
        file_name = category_map.get(category)
        if not file_name:
            return jsonify({
                'success': False,
                'error': 'Invalid category'
            })
        
        file_path = os.path.join('datasets', file_name)
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'Dataset file not found'
            })
        
        prompts = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split by delimiter
            prompt_sections = content.split('---')
            for section in prompt_sections:
                section = section.strip()
                if section:
                    # Extract prompt type (first line) and text (rest)
                    lines = section.split('\n')
                    if lines:
                        prompt_type = lines[0].strip()
                        prompt_text = '\n'.join(lines[1:]).strip()
                        prompts.append({
                            'type': prompt_type,
                            'text': prompt_text
                        })
        
        return jsonify({
            'success': True,
            'prompts': prompts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error loading dataset prompts: {str(e)}'
        })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 LLM Security Testing Web Interface")
    print("="*60)
    print("\n📍 Server starting at: http://127.0.0.1:5000")
    print("\n✨ Features:")
    print("  - View & Generate Dataset")
    print("  - Run Security Tests")
    print("  - View Real-time Results")
    print("  - Generate Reports")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)