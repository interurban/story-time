# Quick Start Guide

## Prerequisites
- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Automated Setup (Recommended)

### Windows
```bash
setup.bat
```

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

## Manual Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and go to [http://localhost:5000](http://localhost:5000)

## Getting an OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the [API Keys page](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key and paste it into your `.env` file

## Troubleshooting

- **Python not found**: Install Python from [python.org](https://python.org/downloads/)
- **Permission errors**: Run terminal as administrator (Windows) or use `sudo` (macOS/Linux)
- **API errors**: Check your OpenAI API key and account credits
- **Port conflicts**: Change the port in `app.py` if 5000 is already in use

## Features

✨ AI-powered story generation using OpenAI GPT  
👶 Age-appropriate content (3-12 years)  
📝 Personalized stories with child's name  
📚 Story management and organization  
📄 PDF export for printing  
🌙 Dark mode for nighttime reading  
📱 Mobile-responsive design  

Happy storytelling! 🌙📚
