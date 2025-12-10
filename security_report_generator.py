import pandas as pd
import json
from datetime import datetime

class SecurityReportGenerator:
    def __init__(self, results_file='security_test_results.csv'):
        self.results_file = results_file
        self.df = None
        try:
            self.df = pd.read_csv(results_file)
        except FileNotFoundError:
            print(f"Warning: {results_file} not found. Report generation will be limited.")
    
    def generate_summary_stats(self):
        """Generate summary statistics"""
        if self.df is None:
            return {}
        
        total_tests = len(self.df)
        successful_tests = len(self.df[self.df['success'] == True])
        refused_tests = len(self.df[self.df['refused'] == True])
        
        # Calculate security score (percentage of refusals among successful tests)
        security_score = (refused_tests / successful_tests * 100) if successful_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'refused_tests': refused_tests,
            'security_score': round(security_score, 2),
            'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_model_comparison(self):
        """Generate comparison by model"""
        if self.df is None:
            return {}
        
        model_stats = {}
        for model in self.df['llm'].unique():
            model_data = self.df[self.df['llm'] == model]
            total = len(model_data)
            successful = len(model_data[model_data['success'] == True])
            refused = len(model_data[model_data['refused'] == True])
            
            security_score = (refused / successful * 100) if successful > 0 else 0
            
            model_stats[model] = {
                'total_tests': total,
                'successful_tests': successful,
                'refused_tests': refused,
                'security_score': round(security_score, 2)
            }
        
        return model_stats
    
    def generate_category_analysis(self):
        """Generate analysis by category"""
        if self.df is None or 'category' not in self.df.columns:
            return {}
        
        category_stats = {}
        for category in self.df['category'].unique():
            if pd.isna(category):
                continue
                
            cat_data = self.df[self.df['category'] == category]
            total = len(cat_data)
            successful = len(cat_data[cat_data['success'] == True])
            refused = len(cat_data[cat_data['refused'] == True])
            
            security_score = (refused / successful * 100) if successful > 0 else 0
            
            category_stats[category] = {
                'total_tests': total,
                'successful_tests': successful,
                'refused_tests': refused,
                'security_score': round(security_score, 2)
            }
        
        return category_stats
    
    def generate_full_report(self):
        """Generate a comprehensive security report"""
        report = {
            'executive_summary': self.generate_summary_stats(),
            'model_comparison': self.generate_model_comparison(),
            'category_analysis': self.generate_category_analysis(),
            'recommendations': self._generate_recommendations()
        }
        
        # Save as JSON
        with open('security_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Also save as markdown report
        self._save_markdown_report(report)
        
        return report
    
    def _generate_recommendations(self):
        """Generate security recommendations"""
        return [
            "Regularly update and patch LLM systems",
            "Implement robust prompt filtering mechanisms",
            "Establish clear usage policies and guidelines",
            "Monitor for unusual interaction patterns",
            "Conduct periodic security assessments",
            "Train users on responsible AI usage",
            "Deploy anomaly detection systems",
            "Maintain audit logs of all interactions"
        ]
    
    def _save_markdown_report(self, report):
        """Save report as markdown"""
        with open('security_report.md', 'w', encoding='utf-8') as f:
            f.write("# LLM Security Test Report\n\n")
            f.write(f"Generated on: {report['executive_summary'].get('generation_date', 'N/A')}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            summary = report['executive_summary']
            f.write(f"- Total Tests Conducted: {summary.get('total_tests', 0)}\n")
            f.write(f"- Successful Tests: {summary.get('successful_tests', 0)}\n")
            f.write(f"- Refused Requests: {summary.get('refused_tests', 0)}\n")
            f.write(f"- Overall Security Score: {summary.get('security_score', 0)}%\n\n")
            
            # Model Comparison
            f.write("## Model Comparison\n\n")
            for model, stats in report['model_comparison'].items():
                f.write(f"### {model}\n")
                f.write(f"- Security Score: {stats['security_score']}%\n")
                f.write(f"- Total Tests: {stats['total_tests']}\n")
                f.write(f"- Refused Requests: {stats['refused_tests']}\n\n")
            
            # Recommendations
            f.write("## Security Recommendations\n\n")
            for rec in report['recommendations']:
                f.write(f"- {rec}\n")

if __name__ == "__main__":
    generator = SecurityReportGenerator()
    report = generator.generate_full_report()
    print("Security report generated successfully!")