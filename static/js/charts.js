// Function to render security scores chart
async function renderSecurityScoresChart() {
    try {
        // Fetch security metrics data
        const response = await fetch('/api/security-metrics');
        const data = await response.json();
        
        if (data.success && Object.keys(data.metrics).length > 0) {
            // Prepare data for chart
            const modelNames = Object.keys(data.metrics);
            const securityScores = modelNames.map(model => data.metrics[model].security_score);
            
            // Get chart canvas
            const ctx = document.getElementById('security-scores-chart');
            if (!ctx) return;
            
            // Create chart
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: modelNames,
                    datasets: [{
                        label: 'Security Score (%)',
                        data: securityScores,
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.7)',
                            'rgba(118, 75, 162, 0.7)',
                            'rgba(72, 187, 120, 0.7)',
                            'rgba(236, 72, 153, 0.7)',
                            'rgba(245, 158, 11, 0.7)'
                        ],
                        borderColor: [
                            'rgb(102, 126, 234)',
                            'rgb(118, 75, 162)',
                            'rgb(72, 187, 120)',
                            'rgb(236, 72, 153)',
                            'rgb(245, 158, 11)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'Security Score (%)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Language Models'
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error rendering security scores chart:', error);
    }
}

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', renderSecurityScoresChart);