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

from flask import Flask, render_template, request, jsonify, send_file
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

app = Flask(__name__)
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

@app.route('/testing')
def testing():
    """Testing page"""
    return render_template('testing.html')

@app.route('/api/start-test', methods=['POST'])
def start_test():
    """Start security testing"""
    global test_progress, test_results
    
    if test_progress['running']:
        return jsonify({
            'success': False,
            'error': 'Test already running'
        })
    
    data = request.json
    selected_llms = data.get('llms', [])
    prompts_per_category = data.get('prompts_per_category', 2)
    
    # Configure models
    models_map = {
        'chatgpt': {'type': 'chatgpt', 'name': 'ChatGPT'},
        'gemini': {'type': 'gemini', 'name': 'Gemini'},
        'deepseek': {'type': 'deepseek', 'name': 'DeepSeek'},
        'qwen': {
            'type': 'huggingface',
            'name': 'QWEN',
            'url': 'https://huggingface.co/spaces/Qwen/Qwen2.5-72B-Instruct'
        },
        'llama': {
            'type': 'huggingface',
            'name': 'Llama',
            'url': 'https://huggingface.co/spaces/meta-llama/Llama-3.2-90B-Vision-Instruct'
        }
    }
    
    models = [models_map[llm] for llm in selected_llms if llm in models_map]
    
    if not models:
        return jsonify({
            'success': False,
            'error': 'No valid LLMs selected'
        })
    
    # Prepare prompts
    all_prompts = get_all_prompts()
    df_prompts = pd.DataFrame(all_prompts)
    sampled = df_prompts.groupby('category').head(prompts_per_category)
    test_prompts = sampled.to_dict('records')
    
    # Reset progress
    test_progress = {
        'running': True,
        'current': 0,
        'total': len(test_prompts) * len(models),
        'status': 'running',
        'current_llm': '',
        'current_category': ''
    }
    test_results = []
    
    # Run tests in background thread
    thread = threading.Thread(target=run_tests_background, args=(test_prompts, models))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': f'Started testing {len(test_prompts)} prompts across {len(models)} models'
    })

def run_tests_background(test_prompts, models):
    """Run tests in background"""
    global test_progress, test_results
    
    tester = LLMSecurityTester(headless=False)
    
    for idx, prompt_data in enumerate(test_prompts):
        prompt = prompt_data['prompt']
        category = prompt_data['category']
        
        for model_config in models:
            test_progress['current_llm'] = model_config['name']
            test_progress['current_category'] = category
            
            tester.setup_driver()
            
            try:
                if model_config['type'] == 'chatgpt':
                    result = tester.test_chatgpt(prompt)
                elif model_config['type'] == 'gemini':
                    result = tester.test_gemini(prompt)
                elif model_config['type'] == 'deepseek':
                    result = tester.test_deepseek(prompt)
                elif model_config['type'] == 'huggingface':
                    result = tester.test_huggingface_model(
                        prompt,
                        model_config['url'],
                        model_config['name']
                    )
                
                result['category'] = category
                result['prompt'] = prompt
                result['timestamp'] = datetime.now().isoformat()
                
                test_results.append(result)
                test_progress['current'] += 1
                
            except Exception as e:
                print(f"Error testing {model_config['name']}: {str(e)}")
                test_progress['current'] += 1
            
            finally:
                tester.close_driver()
                time.sleep(2)
    
    # Save results
    tester.results = test_results
    tester.save_results()
    
    test_progress['running'] = False
    test_progress['status'] = 'completed'

@app.route('/api/test-progress')
def test_progress_api():
    """Get current test progress"""
    return jsonify(test_progress)

@app.route('/results')
def results():
    """Results page"""
    try:
        df = pd.read_csv('security_test_results.csv')
        
        # Calculate summary stats
        summary = {
            'total_tests': len(df),
            'llms_tested': df['llm'].nunique(),
            'categories': df['category'].nunique()
        }
        
        # Security scores
        security_scores = {}
        for llm in df['llm'].unique():
            llm_data = df[df['llm'] == llm]
            successful = len(llm_data[llm_data['success'] == True])
            refusals = len(llm_data[llm_data['refused'] == True])
            score = (refusals / successful * 100) if successful > 0 else 0
            security_scores[llm] = round(score, 2)
        
        results_data = {
            'summary': summary,
            'security_scores': security_scores,
            'has_results': True
        }
    except FileNotFoundError:
        results_data = {'has_results': False}
    
    return render_template('results.html', data=results_data)

@app.route('/api/results')
def api_results():
    """API endpoint for results"""
    try:
        df = pd.read_csv('security_test_results.csv')
        return jsonify({
            'success': True,
            'data': df.to_dict('records')
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'No results found. Run tests first.'
        })

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate comprehensive report"""
    try:
        generator = SecurityReportGenerator('security_test_results.csv')
        generator.generate_full_report()
        
        return jsonify({
            'success': True,
            'message': 'Report generated successfully'
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'No results found. Run tests first.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/security-metrics')
def security_metrics():
    """Get detailed security metrics"""
    try:
        df = pd.read_csv('security_test_results.csv')
        
        metrics = {}
        for llm in df['llm'].unique():
            llm_data = df[df['llm'] == llm]
            total = len(llm_data)
            successful = len(llm_data[llm_data['success'] == True])
            refusals = len(llm_data[llm_data['refused'] == True])
            compliances = len(llm_data[llm_data['refused'] == False])
            
            metrics[llm] = {
                'total_tests': total,
                'successful_tests': successful,
                'refusals': refusals,
                'compliances': compliances,
                'security_score': round((refusals / successful * 100) if successful > 0 else 0, 2),
                'vulnerability_rate': round((compliances / successful * 100) if successful > 0 else 0, 2)
            }
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'No results found'
        })

@app.route('/api/category-analysis')
def category_analysis():
    """Get vulnerability by category"""
    try:
        df = pd.read_csv('security_test_results.csv')
        
        analysis = {}
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            
            category_results = {}
            for llm in df['llm'].unique():
                llm_cat_data = cat_data[cat_data['llm'] == llm]
                if len(llm_cat_data) > 0:
                    refusal_rate = (len(llm_cat_data[llm_cat_data['refused'] == True]) / 
                                   len(llm_cat_data) * 100)
                    category_results[llm] = round(refusal_rate, 2)
            
            analysis[category] = category_results
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'No results found'
        })

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated files"""
    try:
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404

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