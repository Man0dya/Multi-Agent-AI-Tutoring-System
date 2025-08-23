from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import AI agents
import sys
sys.path.append('..')

from agents.content_generator import ContentGeneratorAgent
from agents.question_setter import QuestionSetterAgent
from agents.feedback_evaluator import FeedbackEvaluatorAgent

# Fallback content system for when AI agents are unavailable
class FallbackContentSystem:
    """Provides fallback educational content when AI agents are unavailable"""
    
    @staticmethod
    def get_python_content(topic, difficulty, subject, content_type):
        """Get fallback Python programming content"""
        if "python" in topic.lower():
            return {
                'content': f"""# {topic}

## Introduction
Python is a high-level, interpreted programming language known for its simplicity and readability. It's perfect for beginners and widely used in data science, web development, and automation.

## Key Concepts

### 1. **Variables and Data Types**
- **Variables**: Containers for storing data
- **Strings**: Text data (e.g., `"Hello World"`)
- **Integers**: Whole numbers (e.g., `42`)
- **Floats**: Decimal numbers (e.g., `3.14`)
- **Lists**: Ordered collections (e.g., `[1, 2, 3]`)

### 2. **Basic Syntax**
```python
# This is a comment
name = "Python Learner"  # Variable assignment
age = 25                 # Integer variable
height = 5.9            # Float variable

print(f"Hello {{name}}!")  # String formatting
```

### 3. **Control Structures**
```python
# If statements
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

# Loops
for i in range(5):
    print(f"Count: {{i}}")
```

### 4. **Functions**
```python
def greet(name):
    return f"Hello, {{name}}!"

# Call the function
message = greet("World")
print(message)  # Output: Hello, World!
```

## Real-World Applications
- **Web Development**: Django, Flask frameworks
- **Data Science**: Pandas, NumPy libraries
- **Machine Learning**: Scikit-learn, TensorFlow
- **Automation**: Scripts for repetitive tasks

## Study Tips
1. **Practice Daily**: Code something every day
2. **Start Small**: Begin with simple programs
3. **Use Online Resources**: Python.org, Real Python
4. **Join Communities**: Reddit r/learnpython, Stack Overflow

## Summary
Python is an excellent first programming language. Focus on understanding basic syntax, practice regularly, and build small projects to reinforce your learning.""",
                'key_concepts': [
                    "Variables and Data Types",
                    "Basic Syntax and Comments", 
                    "Control Structures (if/else, loops)",
                    "Functions and Parameters",
                    "String Formatting",
                    "Lists and Collections"
                ],
                'learning_objectives': [
                    "Understand Python syntax and structure",
                    "Create and use variables of different types",
                    "Write basic control structures and loops",
                    "Define and call functions",
                    "Apply Python concepts to solve problems"
                ],
                'study_materials': {
                    "flashcards": [
                        {"term": "Variable", "definition": "A container for storing data in Python"},
                        {"term": "Function", "definition": "A reusable block of code that performs a specific task"},
                        {"term": "Loop", "definition": "A control structure that repeats code multiple times"}
                    ],
                    "summary": "Python basics including variables, data types, control structures, and functions."
                }
            }
        else:
            return {
                'content': f"# {topic}\n\nThis is fallback content for {topic} in {subject}. The AI content generation is currently unavailable due to API rate limits.",
                'key_concepts': ["Basic concepts", "Fundamental principles"],
                'learning_objectives': [f"Understand {topic}", "Apply basic knowledge"],
                'study_materials': {}
            }
    
    @staticmethod
    def get_python_questions(content, question_count, question_types, difficulty):
        """Get fallback Python programming questions"""
        questions = [
            {
                "id": "1",
                "question": "What is a variable in Python?",
                "type": "Multiple Choice",
                "options": [
                    "A mathematical equation",
                    "A container for storing data",
                    "A type of loop",
                    "A function name"
                ],
                "correctAnswer": "A container for storing data",
                "explanation": "Variables in Python are containers that store data values. They can hold different types of data like strings, numbers, and lists.",
                "difficulty": difficulty,
                "bloomLevel": "Understand"
            },
            {
                "id": "2",
                "question": "Which symbol is used for comments in Python?",
                "type": "Multiple Choice",
                "options": [
                    "//",
                    "/*",
                    "#",
                    "--"
                ],
                "correctAnswer": "#",
                "explanation": "In Python, the hash symbol (#) is used to create single-line comments. Comments are not executed by the interpreter.",
                "difficulty": difficulty,
                "bloomLevel": "Remember"
            },
            {
                "id": "3",
                "question": "True or False: Python is a compiled programming language.",
                "type": "True/False",
                "correctAnswer": "False",
                "explanation": "Python is an interpreted language, not compiled. The Python interpreter reads and executes code line by line.",
                "difficulty": difficulty,
                "bloomLevel": "Understand"
            }
        ]
        
        return {
            'questions': questions[:question_count],
            'metadata': {
                'total_count': min(question_count, len(questions)),
                'difficulty_distribution': {difficulty: 1.0},
                'question_types': question_types,
                'bloom_levels': ["Remember", "Understand"],
                'key_concepts_covered': ["Python basics", "Variables", "Comments", "Language types"]
            }
        }

app = FastAPI(title="AI Tutoring System API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI agents
try:
    content_agent = ContentGeneratorAgent()
    question_agent = QuestionSetterAgent()
    feedback_agent = FeedbackEvaluatorAgent()
    print("✅ AI agents initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not initialize AI agents: {e}")
    content_agent = None
    question_agent = None
    feedback_agent = None

# Pydantic models
class ContentRequest(BaseModel):
    topic: str
    subject: str
    difficulty: str
    contentType: str
    learningObjectives: Optional[str] = None

class ContentResponse(BaseModel):
    content: str
    keyConcepts: List[str]
    learningObjectives: List[str]
    studyMaterials: Optional[dict] = None

class QuestionRequest(BaseModel):
    content: str
    questionCount: int
    questionTypes: List[str]
    difficulty: str
    subject: str

class QuestionResponse(BaseModel):
    questions: List[dict]
    metadata: dict

class QuizSubmission(BaseModel):
    questions: List[dict]
    answers: List[dict]
    topic: str

class FeedbackResponse(BaseModel):
    score: int
    feedback: str
    recommendations: List[str]
    detailedAnalysis: dict

@app.get("/")
async def root():
    return {"message": "AI Tutoring System API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents_loaded": all([content_agent, question_agent, feedback_agent])}

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Generate educational content using AI or fallback system"""
    
    try:
        print(f"🎯 Content generation request: {request.topic} for {request.subject}")
        
        # Try to use AI agent first
        if content_agent:
            try:
                print("🤖 Attempting to use AI agent...")
                response = content_agent.generate_content(
                    topic=request.topic,
                    difficulty=request.difficulty,
                    subject=request.subject,
                    content_type=request.contentType,
                    learning_objectives=request.learningObjectives
                )
                
                print("✅ AI agent generated content successfully")
                
                # Extract data from the agent response
                content = response.get('content', '')
                key_concepts = response.get('key_concepts', [])
                learning_objectives = response.get('learning_objectives', [])
                study_materials = response.get('study_materials', {})
                
                # If key_concepts or learning_objectives are empty, extract them from content
                if not key_concepts and content:
                    key_concepts = extract_key_concepts_from_content(content)
                
                if not learning_objectives and content:
                    learning_objectives = extract_learning_objectives_from_content(content, request.topic)
                
                return ContentResponse(
                    content=content,
                    keyConcepts=key_concepts,
                    learningObjectives=learning_objectives,
                    studyMaterials=study_materials
                )
                
            except Exception as ai_error:
                print(f"❌ AI agent failed: {ai_error}")
                # Fall through to fallback system
        
        # Use fallback content system when AI agents fail
        print("🔄 Using fallback content system...")
        fallback_response = FallbackContentSystem.get_python_content(
            topic=request.topic,
            difficulty=request.difficulty,
            subject=request.subject,
            content_type=request.contentType
        )
        
        print("✅ Fallback content generated successfully")
        
        return ContentResponse(
            content=fallback_response['content'],
            keyConcepts=fallback_response['key_concepts'],
            learningObjectives=fallback_response['learning_objectives'],
            studyMaterials=fallback_response['study_materials']
        )
        
    except Exception as e:
        print(f"💥 Content generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {str(e)}")

def extract_key_concepts_from_content(content):
    """Extract key concepts from AI-generated content"""
    try:
        # Look for headers and bullet points that indicate key concepts
        lines = content.split('\n')
        concepts = []
        
        for line in lines:
            line = line.strip()
            # Look for headers (lines starting with # or ##)
            if line.startswith('##') and len(line) > 3:
                concept = line.replace('#', '').replace('*', '').strip()
                if concept and len(concept) < 100:
                    concepts.append(concept)
            # Look for bullet points with key concepts
            elif line.startswith('*') and '**' in line:
                # Extract text between ** **
                import re
                matches = re.findall(r'\*\*(.*?)\*\*', line)
                concepts.extend(matches)
        
        # If we found concepts, return them; otherwise return some default ones
        if concepts:
            return concepts[:10]  # Limit to 10 concepts
        else:
            return [
                "Core Principles",
                "Key Components", 
                "Fundamental Concepts",
                "Main Applications",
                "Important Methods"
            ]
    except Exception:
        return ["Core Principles", "Key Components", "Fundamental Concepts"]

def extract_learning_objectives_from_content(content, topic):
    """Extract learning objectives from AI-generated content"""
    try:
        # Look for sections about learning objectives or study tips
        lines = content.split('\n')
        objectives = []
        
        # Look for common patterns in learning objectives
        for line in lines:
            line = line.strip().lower()
            if any(keyword in line for keyword in ['understand', 'learn', 'identify', 'apply', 'analyze', 'create']):
                if len(line) > 20 and len(line) < 200:
                    objectives.append(line.capitalize())
        
        # If we found objectives, return them; otherwise return default ones
        if objectives:
            return objectives[:5]  # Limit to 5 objectives
        else:
            return [
                f"Understand the core concepts of {topic}",
                f"Identify key components and principles of {topic}",
                f"Apply {topic} knowledge to practical scenarios",
                f"Analyze real-world applications of {topic}",
                f"Evaluate different approaches within {topic}"
            ]
    except Exception:
        return [
            f"Understand the core concepts of {topic}",
            f"Apply {topic} knowledge to practical scenarios",
            f"Analyze real-world applications of {topic}"
        ]

@app.post("/api/generate-questions", response_model=QuestionResponse)
async def generate_questions(request: QuestionRequest):
    """Generate assessment questions using AI or fallback system"""
    
    try:
        print(f"🎯 Question generation request: {request.questionCount} questions for {request.subject}")
        
        # Try to use AI agent first
        if question_agent:
            try:
                print("🤖 Attempting to use AI agent...")
                response = question_agent.generate_questions(
                    content=request.content,
                    question_count=request.questionCount,
                    question_types=request.questionTypes,
                    difficulty_distribution={"Easy": 0.3, "Medium": 0.5, "Hard": 0.2}
                )
                
                print("✅ AI agent generated questions successfully")
                
                # Extract questions and metadata from the agent response
                questions = response.get('questions', [])
                metadata = response.get('metadata', {})
                
                # Ensure questions have the expected structure
                formatted_questions = []
                for i, question in enumerate(questions):
                    formatted_question = {
                        "id": str(i + 1),
                        "question": question.get('question', ''),
                        "type": question.get('type', 'Multiple Choice'),
                        "options": question.get('options', []),
                        "correctAnswer": question.get('correct_answer', ''),
                        "explanation": question.get('explanation', ''),
                        "difficulty": question.get('difficulty', request.difficulty),
                        "bloomLevel": question.get('bloom_level', 'Understand')
                    }
                    formatted_questions.append(formatted_question)
                
                return QuestionResponse(
                    questions=formatted_questions,
                    metadata={
                        "topic": "Generated from provided content",
                        "subject": request.subject,
                        "difficulty": request.difficulty,
                        "questionTypes": request.questionTypes,
                        **metadata
                    }
                )
                
            except Exception as ai_error:
                print(f"❌ AI agent failed: {ai_error}")
                # Fall through to fallback system
        
        # Use fallback question system when AI agents fail
        print("🔄 Using fallback question system...")
        fallback_response = FallbackContentSystem.get_python_questions(
            content=request.content,
            question_count=request.questionCount,
            question_types=request.questionTypes,
            difficulty=request.difficulty
        )
        
        print("✅ Fallback questions generated successfully")
        
        # Format fallback questions to match expected structure
        formatted_questions = []
        for question in fallback_response['questions']:
            formatted_question = {
                "id": question['id'],
                "question": question['question'],
                "type": question['type'],
                "options": question.get('options', []),
                "correctAnswer": question['correctAnswer'],
                "explanation": question['explanation'],
                "difficulty": question['difficulty'],
                "bloomLevel": question['bloomLevel']
            }
            formatted_questions.append(formatted_question)
        
        return QuestionResponse(
            questions=formatted_questions,
            metadata=fallback_response['metadata']
        )
        
    except Exception as e:
        print(f"💥 Question generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

@app.post("/api/evaluate-quiz", response_model=FeedbackResponse)
async def evaluate_quiz(submission: QuizSubmission):
    """Evaluate quiz answers and provide feedback using AI or fallback system"""
    
    try:
        print(f"🎯 Quiz evaluation request for topic: {submission.topic}")
        
        # Try to use AI agent first
        if feedback_agent:
            try:
                print("🤖 Attempting to use AI agent...")
                # Convert answers to the format expected by the feedback agent
                user_answers = {}
                for i, answer in enumerate(submission.answers):
                    user_answers[i] = answer.get('answer', '')
                
                # Evaluate answers using the AI agent with correct parameters
                response = feedback_agent.evaluate_answers(
                    questions=submission.questions,
                    user_answers=user_answers,
                    feedback_type="Detailed",
                    include_suggestions=True
                )
                
                print("✅ AI agent evaluated quiz successfully")
                
                # Extract feedback data from the agent response
                overall_score = response.get('overall_score', 0)
                detailed_feedback = response.get('detailed_feedback', '')
                study_suggestions = response.get('study_suggestions', '')
                learning_analysis = response.get('learning_analysis', {})
                
                # Convert to the expected response format
                recommendations = []
                if study_suggestions:
                    # Split study suggestions into recommendations
                    suggestions = study_suggestions.split('.')
                    recommendations = [s.strip() for s in suggestions if s.strip()]
                
                detailed_analysis = {
                    "strengths": learning_analysis.get('strengths', []),
                    "weaknesses": learning_analysis.get('weaknesses', []),
                    "areas_for_improvement": learning_analysis.get('areas_for_improvement', [])
                }
                
                return FeedbackResponse(
                    score=int(overall_score),
                    feedback=detailed_feedback,
                    recommendations=recommendations,
                    detailedAnalysis=detailed_analysis
                )
                
            except Exception as ai_error:
                print(f"❌ AI agent failed: {ai_error}")
                # Fall through to fallback system
        
        # Use fallback feedback system when AI agents fail
        print("🔄 Using fallback feedback system...")
        # Simple scoring based on correct answers
        correct_count = 0
        total_questions = len(submission.questions)
        
        for i, question in enumerate(submission.questions):
            user_answer = submission.answers[i].get('answer', '')
            correct_answer = question.get('correctAnswer', '')
            
            if user_answer.lower().strip() == correct_answer.lower().strip():
                correct_count += 1
        
        score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
        
        # Generate basic feedback
        if score >= 80:
            feedback = "Excellent work! You have a strong understanding of the material."
        elif score >= 60:
            feedback = "Good job! You understand most concepts but could review some areas."
        else:
            feedback = "Keep studying! Review the material and practice more to improve your understanding."
        
        recommendations = [
            "Review the questions you missed",
            "Practice with similar problems",
            "Focus on understanding the underlying concepts"
        ]
        
        detailed_analysis = {
            "strengths": [f"Correctly answered {correct_count} out of {total_questions} questions"],
            "weaknesses": [f"Missed {total_questions - correct_count} questions"],
            "areas_for_improvement": ["Review incorrect answers", "Practice more problems"]
        }
        
        print("✅ Fallback feedback generated successfully")
        
        return FeedbackResponse(
            score=score,
            feedback=feedback,
            recommendations=recommendations,
            detailedAnalysis=detailed_analysis
        )
        
    except Exception as e:
        print(f"💥 Quiz evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to evaluate quiz: {str(e)}")

@app.get("/api/subjects")
async def get_subjects():
    """Get available subjects"""
    return {
        "subjects": [
            "Computer Science", "Mathematics", "Physics", "Chemistry",
            "Biology", "History", "Literature", "Languages", "Business", "Arts"
        ]
    }

@app.get("/api/content-types")
async def get_content_types():
    """Get available content types"""
    return {
        "contentTypes": [
            "Study Notes", "Tutorial", "Explanation", "Summary", "Comprehensive Guide"
        ]
    }

@app.get("/api/question-types")
async def get_question_types():
    """Get available question types"""
    return {
        "questionTypes": [
            "Multiple Choice", "True/False", "Short Answer", "Essay", "Fill in the Blank"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
