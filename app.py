from flask import Flask, render_template, request, jsonify
import os
import requests

# Initialize Flask app
app = Flask(__name__)

# NVIDIA API configuration 
API_KEY = os.getenv('API_KEY')
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"  
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    prompt = data.get('prompt', '')
    content_type = data.get('content_type', 'blog')
    length = data.get('length', 'medium')
    
    # Length parameters
    length_guide = {
        'short': 'around 250 words',
        'medium': 'around 500 words',
        'long': 'around 1000 words'
    }
    
    # Create system instructions based on content type
    system_instructions = {
        'blog': f"Write a well-structured blog post about: {prompt}. Make it engaging and informative, {length_guide[length]}.",
        'social': f"Create engaging social media content about: {prompt}. Make it catchy and shareable, {length_guide[length]}.",
        'email': f"Write a professional email about: {prompt}. Keep it clear and actionable, {length_guide[length]}.",
        'product': f"Write compelling product description copy for: {prompt}. Focus on benefits and features, {length_guide[length]}."
    }
    
    try:
        # Call the NVIDIA API
        response = query_nvidia_api(system_instructions.get(content_type, f"Write content about: {prompt}. Keep it {length_guide[length]}."))
        
        if isinstance(response, dict) and 'error' in response:
            return jsonify({"error": response['error']}), 500
            
        return jsonify({"content": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def query_nvidia_api(user_message):
    """
    Query the NVIDIA API using the chat completions endpoint
    """
    try:
        payload = {
            "model": "meta/llama-3.1-405b-instruct",  # Using a supported model
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that creates high-quality content. Always provide complete, well-formatted responses."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 1024
        }
        
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # Extract the generated text from the response
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return content
            else:
                return {"error": "No content generated"}
        else:
            error_msg = f"API request failed with status code: {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f" - {error_detail}"
            except:
                error_msg += f" - {response.text}"
            return {"error": error_msg}
    
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Error querying NVIDIA API: {str(e)}"}

# Create templates directory and HTML file
def create_template_files():
    os.makedirs('templates', exist_ok=True)
    
    with open('templates/index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Write Eye: AI Content Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --secondary: #64748b;
            --background: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --border-radius: 12px;
            --transition: all 0.3s ease;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--background);
            color: var(--text);
            padding: 2rem 0;
            min-height: 100vh;
        }
        
        .container {
            max-width: 900px;
        }
        
        .app-header {
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .app-title {
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }
        
        .app-subtitle {
            color: var(--secondary);
            font-weight: 500;
        }
        
        .card {
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            border: none;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            transition: var(--transition);
            overflow: hidden;
            margin-bottom: 2rem;
        }
        
        .card:hover {
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--primary), var(--primary-hover));
            color: white;
            border-bottom: none;
            padding: 1.5rem;
        }
        
        .card-body {
            padding: 2rem;
        }
        
        .form-label {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text);
        }
        
        .form-control, .form-select {
            border-radius: 8px;
            padding: 0.75rem 1rem;
            border: 1px solid #e2e8f0;
            background-color: #f8fafc;
            transition: var(--transition);
        }
        
        .form-control:focus, .form-select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
            background-color: white;
        }
        
        .btn-primary {
            background-color: var(--primary);
            border-color: var(--primary);
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: var(--transition);
        }
        
        .btn-primary:hover:not(:disabled) {
            background-color: var(--primary-hover);
            border-color: var(--primary-hover);
            transform: translateY(-2px);
        }
        
        .btn-primary:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
        
        #result {
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: auto;
            padding: 1.5rem;
            background-color: #f8fafc;
            border-radius: 8px;
            font-size: 0.95rem;
            line-height: 1.6;
            border: 1px solid #e2e8f0;
        }
        
        .spinner-border {
            color: var(--primary) !important;
            width: 2rem;
            height: 2rem;
        }
        
        .error-message {
            background-color: #fef2f2;
            color: #dc2626;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #fecaca;
        }
        
        .features-list {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 3rem;
            flex-wrap: wrap;
        }
        
        .feature-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            max-width: 180px;
        }
        
        .feature-icon {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .feature-desc {
            color: var(--secondary);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="app-header">
            <h1 class="app-title">Write Eye: AI Content Generator</h1>
            <p class="app-subtitle">Create high-quality content in seconds with NVIDIA AI</p>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h2 class="mb-0 fs-4 text-center">Create Your Content</h2>
            </div>
            <div class="card-body">
                <form id="generatorForm">
                    <div class="mb-3">
                        <label for="promptInput" class="form-label">What would you like to write about?</label>
                        <textarea class="form-control" id="promptInput" rows="3" placeholder="Describe your topic or provide specific details for better results..." required></textarea>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="contentType" class="form-label">Content Type</label>
                            <select class="form-select" id="contentType">
                                <option value="blog">Blog Post</option>
                                <option value="social">Social Media</option>
                                <option value="email">Email</option>
                                <option value="product">Product Description</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="contentLength" class="form-label">Length</label>
                            <select class="form-select" id="contentLength">
                                <option value="short">Short (~250 words)</option>
                                <option value="medium" selected>Medium (~500 words)</option>
                                <option value="long">Long (~1000 words)</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary" id="generateBtn">
                            <i class="fas fa-magic me-2"></i> Generate Content
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <div class="text-center my-4">
            <div class="spinner-border d-none" role="status" id="loadingSpinner">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        
        <div class="card d-none" id="resultCard">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h3 class="mb-0 fs-4">Generated Content</h3>
                <button class="btn btn-sm btn-outline-light" id="copyBtn">
                    <i class="fas fa-copy me-1"></i> Copy
                </button>
            </div>
            <div class="card-body">
                <div id="result"></div>
            </div>
        </div>
        
        <div class="features-list">
            <div class="feature-item">
                <i class="fas fa-bolt feature-icon"></i>
                <h3 class="feature-title">Fast Generation</h3>
                <p class="feature-desc">Get high-quality content in seconds</p>
            </div>
            <div class="feature-item">
                <i class="fas fa-robot feature-icon"></i>
                <h3 class="feature-title">AI Powered</h3>
                <p class="feature-desc">Using NVIDIA's advanced language models</p>
            </div>
            <div class="feature-item">
                <i class="fas fa-layer-group feature-icon"></i>
                <h3 class="feature-title">Multiple Formats</h3>
                <p class="feature-desc">Blogs, social posts, emails and more</p>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.getElementById('generatorForm');
            const resultCard = document.getElementById('resultCard');
            const resultDiv = document.getElementById('result');
            const loadingSpinner = document.getElementById('loadingSpinner');
            const generateBtn = document.getElementById('generateBtn');
            const copyBtn = document.getElementById('copyBtn');
            
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const prompt = document.getElementById('promptInput').value.trim();
                if (!prompt) {
                    alert('Please enter a topic or description');
                    return;
                }
                
                const contentType = document.getElementById('contentType').value;
                const length = document.getElementById('contentLength').value;
                
                // Show loading state
                generateBtn.disabled = true;
                generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
                loadingSpinner.classList.remove('d-none');
                resultCard.classList.add('d-none');
                
                // Send request to backend
                fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        content_type: contentType,
                        length: length
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    // Reset button state
                    generateBtn.disabled = false;
                    generateBtn.innerHTML = '<i class="fas fa-magic me-2"></i> Generate Content';
                    loadingSpinner.classList.add('d-none');
                    
                    if (data.error) {
                        resultDiv.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle me-2"></i>${data.error}</div>`;
                        resultCard.classList.remove('d-none');
                        return;
                    }
                    
                    // Display the result
                    resultDiv.textContent = data.content;
                    resultCard.classList.remove('d-none');
                    resultCard.scrollIntoView({ behavior: 'smooth' });
                })
                .catch(error => {
                    // Reset button state
                    generateBtn.disabled = false;
                    generateBtn.innerHTML = '<i class="fas fa-magic me-2"></i> Generate Content';
                    loadingSpinner.classList.add('d-none');
                    
                    resultDiv.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle me-2"></i>Network error: ${error.message}</div>`;
                    resultCard.classList.remove('d-none');
                });
            });
            
            // Copy button functionality
            copyBtn.addEventListener('click', function() {
                const content = resultDiv.textContent;
                navigator.clipboard.writeText(content)
                    .then(() => {
                        const originalHTML = copyBtn.innerHTML;
                        copyBtn.innerHTML = '<i class="fas fa-check me-1"></i> Copied!';
                        copyBtn.classList.remove('btn-outline-light');
                        copyBtn.classList.add('btn-success');
                        setTimeout(() => {
                            copyBtn.innerHTML = originalHTML;
                            copyBtn.classList.remove('btn-success');
                            copyBtn.classList.add('btn-outline-light');
                        }, 2000);
                    })
                    .catch(err => {
                        alert('Failed to copy: ' + err);
                    });
            });
        });
    </script>
</body>
</html>''')

if __name__ == '__main__':
    create_template_files()
    print("Template files created successfully!")
    print("Flask app starting...")
    print("Visit http://127.0.0.1:5000 to access the app")
    app.run(debug=True, host='0.0.0.0', port=5000)