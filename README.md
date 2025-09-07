# Multi-Agent AI Tutoring System 🎓

A sophisticated AI-powered educational platform that uses multiple specialized AI agents to create personalized learning experiences. Built with React, FastAPI, and Google Gemini AI.

## ✨ Features

### 🤖 AI Agents
- **Content Generator Agent**: Creates engaging, personalized educational content
- **Question Setter Agent**: Generates assessment questions from content
- **Feedback Evaluator Agent**: Provides intelligent feedback and scoring

### 🎯 Content Generation
- Dynamic, natural content creation (no rigid templates!)
- Multiple content types: Tutorials, Study Notes, Explanations, Summaries
- Adaptive difficulty levels (Beginner, Intermediate, Advanced)
- Subject-specific content across multiple disciplines

### 📚 Question Generation
- Multiple question types: Multiple Choice, True/False, Short Answer, Essay
- Bloom's Taxonomy integration for cognitive complexity
- Difficulty-based question generation
- Comprehensive explanations and feedback

### 🧠 Smart Evaluation
- AI-powered answer evaluation
- Personalized feedback and recommendations
- Learning progress tracking
- Adaptive difficulty adjustment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   FastAPI Backend│    │  Google Gemini  │
│                 │◄──►│                 │◄──►│      AI API     │
│   - TypeScript  │    │   - Python      │    │                 │
│   - Tailwind CSS│    │   - Pydantic    │    │                 │
│   - Vite        │    │   - Uvicorn     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for modern, responsive design
- **React Router** for navigation
- **Lucide React** for beautiful icons

### Backend
- **FastAPI** for high-performance API
- **Python 3.13** for AI agent logic
- **Google Gemini AI** for content generation
- **MongoDB** for data persistence
- **Pydantic** for data validation

### AI & ML
- **Google Generative AI** (Gemini 2.0 Flash)
- **NLTK** for natural language processing
- **Custom AI agents** for specialized tasks
- **Fallback content system** for reliability

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (local or Atlas)
- Google Gemini API key

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Man0dya/Multi-Agent-AI-Tutoring-System.git
cd Multi-Agent-AI-Tutoring-System

# Install Python dependencies
cd api
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys and MongoDB URI

# Start the backend
python main.py
```

### Frontend Setup
```bash
# Install Node.js dependencies
cd react-frontend-new
npm install

# Start the development server
npm run dev
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `api` directory:

```env
# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# MongoDB
MONGODB_URI=your_mongodb_connection_string
MONGODB_DATABASE=tutoring_system

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

### MongoDB Setup
The system supports both local MongoDB and MongoDB Atlas:
- **Local**: Install MongoDB Community Edition
- **Atlas**: Use your cloud MongoDB instance

## 🎮 Usage

### 1. Content Generation
- Navigate to Content Generator
- Select topic, subject, difficulty, and content type
- Click "Generate Content" to create AI-powered educational materials

### 2. Question Generation
- Use generated content or paste your own
- Select question types and count
- Generate assessment questions with AI

### 3. Interactive Quiz
- Take quizzes with generated questions
- Get AI-powered feedback and scoring
- Track learning progress

## 🔍 API Endpoints

### Content Generation
```http
POST /api/generate-content
{
  "topic": "Machine Learning",
  "subject": "Computer Science",
  "difficulty": "Intermediate",
  "contentType": "Tutorial"
}
```

### Question Generation
```http
POST /api/generate-questions
{
  "content": "Your content here",
  "questionCount": 5,
  "questionTypes": ["Multiple Choice", "True/False"],
  "difficulty": "Medium",
  "subject": "Computer Science"
}
```

### Quiz Evaluation
```http
POST /api/evaluate-quiz
{
  "questions": [...],
  "answers": [...],
  "topic": "Quiz Topic"
}
```

## 🧪 Testing

### Backend Testing
```bash
cd api
python -m pytest tests/
```

### Frontend Testing
```bash
cd react-frontend-new
npm test
```

## 📁 Project Structure

```
Multi-Agent-AI-Tutoring-System/
├── api/                          # FastAPI backend
│   ├── main.py                  # Main application
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment template
├── agents/                      # AI agent implementations
│   ├── content_generator.py    # Content generation agent
│   ├── question_setter.py      # Question generation agent
│   └── feedback_evaluator.py   # Feedback evaluation agent
├── react-frontend-new/          # React frontend
│   ├── src/                    # Source code
│   ├── package.json            # Node.js dependencies
│   └── vite.config.ts          # Vite configuration
├── utils/                       # Utility functions
│   └── nlp_processor.py        # NLP processing utilities
├── models/                      # Data models
│   └── mongodb_models.py       # MongoDB schemas
├── services/                    # Business logic
│   └── mongodb_service.py      # Database operations
├── config/                      # Configuration files
│   └── mongodb_config.py       # MongoDB configuration
├── scripts/                     # Utility scripts
│   └── migrate_to_mongodb.py   # Database migration
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🌟 Key Features

### Natural Content Generation
- **No rigid templates** - Content flows naturally
- **Varied sentence structures** for engaging reading
- **Conversational tone** like a knowledgeable teacher
- **Adaptive content styles** based on content type

### Intelligent Question Generation
- **Context-aware** question creation
- **Difficulty scaling** based on content complexity
- **Multiple question types** for comprehensive assessment
- **Bloom's Taxonomy** integration for cognitive development

### Smart Feedback System
- **AI-powered evaluation** of answers
- **Personalized recommendations** for improvement
- **Learning progress tracking** over time
- **Adaptive difficulty adjustment**

## 🔒 Security Features

- **CORS protection** for cross-origin requests
- **Environment variable** management for sensitive data
- **Input validation** with Pydantic models
- **Rate limiting** for API protection

## 🚀 Performance Features

- **Async FastAPI** for high concurrency
- **MongoDB indexing** for fast queries
- **React optimization** with Vite
- **Efficient AI processing** with Gemini API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful content generation
- **FastAPI** for high-performance backend framework
- **React** for modern frontend development
- **MongoDB** for flexible data storage
- **OpenAI** for inspiration in AI agent architecture

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Man0dya/Multi-Agent-AI-Tutoring-System/issues)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Man0dya/Multi-Agent-AI-Tutoring-System&type=Date)](https://star-history.com/#Man0dya/Multi-Agent-AI-Tutoring-System&Date)

---


**Built with ❤️ by the Multi-Agent AI Tutoring System Team**

*Empowering education through intelligent AI agents*




