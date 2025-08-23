# AI Tutoring System - FastAPI Backend

A FastAPI backend that provides REST API endpoints for the AI Tutoring System, integrating with the existing AI agents.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🤖 **AI Agent Integration** - Connects with Content Generator, Question Setter, and Feedback Evaluator
- 🔒 **CORS Support** - Configured for React frontend integration
- 📊 **Pydantic Models** - Type-safe request/response handling
- 🔌 **MongoDB Integration** - Database connectivity for persistent storage

## API Endpoints

### Health & Status
- `GET /` - API root and status
- `GET /health` - Health check with agent status

### Content Generation
- `POST /api/generate-content` - Generate educational content using AI
- `GET /api/subjects` - Get available subjects
- `GET /api/content-types` - Get available content types

### Question Generation
- `POST /api/generate-questions` - Generate assessment questions using AI
- `GET /api/question-types` - Get available question types

### Quiz Evaluation
- `POST /api/evaluate-quiz` - Evaluate quiz answers and provide AI feedback

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB (optional, for full functionality)
- Google Generative AI API key

### Installation

1. Navigate to the API directory:
```bash
cd api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
GEMINI_API_KEY=your_api_key_here
MONGODB_URI=your_mongodb_connection_string
MONGODB_DATABASE=tutor_ai
```

4. Start the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Development Server

For development with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

## Request/Response Examples

### Generate Content
```bash
curl -X POST "http://localhost:8000/api/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Machine Learning",
    "subject": "Computer Science",
    "difficulty": "Intermediate",
    "contentType": "Study Notes",
    "learningObjectives": "Understand ML fundamentals"
  }'
```

### Generate Questions
```bash
curl -X POST "http://localhost:8000/api/generate-questions" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Machine learning is a subset of artificial intelligence...",
    "questionCount": 5,
    "questionTypes": ["Multiple Choice", "True/False"],
    "difficulty": "Medium",
    "subject": "Computer Science"
  }'
```

## Integration with React Frontend

The API is configured with CORS to work with the React frontend running on `http://localhost:3000`. The frontend can make requests to these endpoints to:

1. Generate educational content
2. Create assessment questions
3. Submit quizzes for evaluation
4. Get personalized feedback

## Error Handling

The API includes comprehensive error handling:
- Input validation using Pydantic models
- AI agent availability checks
- Graceful fallbacks when agents are unavailable
- Detailed error messages for debugging

## Future Enhancements

- User authentication and authorization
- Rate limiting and API key management
- WebSocket support for real-time updates
- Advanced caching strategies
- Analytics and usage tracking
