from datetime import datetime
from typing import Dict, List, Any, Optional
from bson import ObjectId

class ContentModel:
    """MongoDB model for educational content"""
    
    @staticmethod
    def create_content(
        title: str,
        content: str,
        subject: str,
        topic: str,
        content_type: str = "lesson",
        difficulty: str = "intermediate",
        learning_objectives: List[str] = None,
        key_concepts: List[str] = None,
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """Create a content document"""
        return {
            "title": title,
            "content": content,
            "subject": subject.lower(),
            "topic": topic.lower(),
            "content_type": content_type,
            "difficulty": difficulty.lower(),
            "learning_objectives": learning_objectives or [],
            "key_concepts": key_concepts or [],
            "tags": tags or [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "views": 0,
            "rating": 0.0,
            "ratings_count": 0
        }
    
    @staticmethod
    def update_content(content_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update content document"""
        updates["updated_at"] = datetime.utcnow()
        return {"$set": updates}

class UserProgressModel:
    """MongoDB model for user learning progress"""
    
    @staticmethod
    def create_progress(
        user_id: str,
        subject: str,
        topic: str,
        score: float,
        total_questions: int,
        correct_answers: int,
        time_spent: int = 0,
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """Create a user progress document"""
        return {
            "user_id": user_id,
            "subject": subject.lower(),
            "topic": topic.lower(),
            "score": score,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "time_spent": time_spent,
            "difficulty": difficulty.lower(),
            "timestamp": datetime.utcnow(),
            "performance_level": UserProgressModel._calculate_performance_level(score)
        }
    
    @staticmethod
    def _calculate_performance_level(score: float) -> str:
        """Calculate performance level based on score"""
        if score >= 90:
            return "excellent"
        elif score >= 80:
            return "good"
        elif score >= 70:
            return "satisfactory"
        elif score >= 60:
            return "needs_improvement"
        else:
            return "requires_attention"

class QuestionModel:
    """MongoDB model for assessment questions"""
    
    @staticmethod
    def create_question(
        question: str,
        question_type: str,
        subject: str,
        topic: str,
        difficulty: str,
        bloom_level: str,
        correct_answer: str,
        options: List[str] = None,
        explanation: str = None,
        key_points: List[str] = None,
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """Create a question document"""
        return {
            "question": question,
            "question_type": question_type.lower(),
            "subject": subject.lower(),
            "topic": topic.lower(),
            "difficulty": difficulty.lower(),
            "bloom_level": bloom_level.lower(),
            "correct_answer": correct_answer,
            "options": options or [],
            "explanation": explanation or "",
            "key_points": key_points or [],
            "tags": tags or [],
            "created_at": datetime.utcnow(),
            "usage_count": 0,
            "success_rate": 0.0,
            "average_time": 0
        }

class UserModel:
    """MongoDB model for user accounts"""
    
    @staticmethod
    def create_user(
        username: str,
        email: str,
        learning_preferences: Dict[str, Any] = None,
        subjects_of_interest: List[str] = None
    ) -> Dict[str, Any]:
        """Create a user document"""
        return {
            "username": username,
            "email": email,
            "learning_preferences": learning_preferences or {
                "difficulty_preference": "medium",
                "preferred_subjects": [],
                "learning_style": "visual",
                "daily_goal": 30
            },
            "subjects_of_interest": subjects_of_interest or [],
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "total_study_time": 0,
            "completed_topics": [],
            "achievements": []
        }

class StudySessionModel:
    """MongoDB model for study sessions"""
    
    @staticmethod
    def create_session(
        user_id: str,
        subject: str,
        topic: str,
        session_type: str = "practice"
    ) -> Dict[str, Any]:
        """Create a study session document"""
        return {
            "user_id": user_id,
            "subject": subject.lower(),
            "topic": topic.lower(),
            "session_type": session_type,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "duration": 0,
            "questions_answered": 0,
            "correct_answers": 0,
            "score": 0.0,
            "status": "active"
        }
    
    @staticmethod
    def end_session(session_id: str, final_score: float, duration: int) -> Dict[str, Any]:
        """End a study session"""
        return {
            "$set": {
                "end_time": datetime.utcnow(),
                "duration": duration,
                "score": final_score,
                "status": "completed"
            }
        }
