# MongoDB Configuration Template
# Copy this to your .env file or set these environment variables

MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DATABASE = "tutor_ai"

# For MongoDB Atlas (cloud), use:
# MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
# MONGODB_DATABASE = "tutor_ai_production"

# Google Gemini API (for AI features)
GEMINI_API_KEY = "your_gemini_api_key_here"

# App Configuration
STREAMLIT_SERVER_PORT = 8502
STREAMLIT_SERVER_ADDRESS = "127.0.0.1"

# Example .env file content:
"""
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=tutor_ai
GEMINI_API_KEY=your_actual_api_key_here
STREAMLIT_SERVER_PORT=8502
STREAMLIT_SERVER_ADDRESS=127.0.0.1
"""
