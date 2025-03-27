# Write-Eye
# Write Eye: AI Content Generator 🚀✍️

## Overview
Write Eye is a Flask-based web application that leverages the Mistral-7B-Instruct language model via Hugging Face's Inference API to generate high-quality content across multiple formats quickly and easily.

## 🌟 Key Features

### Content Generation Capabilities
- **Multiple Content Types**:
  - Blog Posts
  - Social Media Content
  - Professional Emails
  - Product Descriptions

### Flexible Content Customization
- **Length Options**:
  - Short (~250 words)
  - Medium (~500 words)
  - Long (~1000 words)

### User-Friendly Interface
- Clean, modern Bootstrap-based design
- Responsive layout
- Real-time content generation
- Easy copy-to-clipboard functionality

## 🛠 Technical Architecture

### Backend
- **Framework**: Flask
- **AI Model**: Mistral-7B-Instruct (Hugging Face)
- **API Integration**: Hugging Face Inference API

### Frontend
- **Technologies**: 
  - HTML5
  - Bootstrap 5
  - Font Awesome icons
  - Vanilla JavaScript

## 🚀 How It Works

1. **User Input**:
   - Enter a topic or description
   - Select content type
   - Choose desired content length

2. **AI Generation Process**:
   - Constructs a specialized prompt for the Mistral model
   - Sends request to Hugging Face API
   - Processes and returns generated content

3. **Content Display**:
   - Instantly shows generated text
   - Provides copy functionality
   - Responsive design across devices
  
     
   ![image](https://github.com/user-attachments/assets/06ef4d67-f3c7-47da-b5dd-7f02cb28d05f)


## 🔧 Getting Started

### Prerequisites
- Python 3.8+
- Flask
- requests library
- Hugging Face API Token

### Installation
```bash
git clone https://github.com/yourusername/write-eye.git
cd write-eye
pip install flask requests
python app.py
```

## 🔒 Important Notes
- Replace `HF_API_TOKEN` with your own Hugging Face API token
- Ensure you have internet connectivity for API calls

## 🌈 Future Roadmap
- Add more content type templates
- Implement advanced prompt engineering
- Create user authentication
- Add content export options

## 📝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/jaswanthbandaru/write-eye/issues).

## 📄 License
[Specify your license here, e.g., MIT]

---

*Powered by Mistral AI and Hugging Face* 🤖📝
