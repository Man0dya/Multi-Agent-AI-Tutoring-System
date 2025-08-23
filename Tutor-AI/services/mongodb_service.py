from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from bson import ObjectId
from config.mongodb_config import mongodb_config
from models.mongodb_models import (
    ContentModel, UserProgressModel, QuestionModel, 
    UserModel, StudySessionModel
)

class MongoDBService:
    """Service layer for MongoDB operations"""
    
    def __init__(self):
        self.db = mongodb_config.get_database()
        self.content_collection = self.db['content']
        self.progress_collection = self.db['user_progress']
        self.questions_collection = self.db['questions']
        self.users_collection = self.db['users']
        self.sessions_collection = self.db['study_sessions']
    
    # Content Management
    def add_content(self, content_data: Dict[str, Any]) -> str:
        """Add new educational content"""
        try:
            content_doc = ContentModel.create_content(**content_data)
            result = self.content_collection.insert_one(content_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error adding content: {e}")
            return None
    
    def get_content_by_subject(self, subject: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get content by subject"""
        try:
            cursor = self.content_collection.find(
                {"subject": subject.lower()}
            ).sort("created_at", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error getting content: {e}")
            return []
    
    def search_content(self, query: str, subject: str = None) -> List[Dict[str, Any]]:
        """Search content using text search"""
        try:
            search_filter = {"$text": {"$search": query}}
            if subject:
                search_filter["subject"] = subject.lower()
            
            cursor = self.content_collection.find(search_filter).sort("score", {"$meta": "textScore"})
            return list(cursor)
        except Exception as e:
            print(f"Error searching content: {e}")
            return []
    
    def update_content_views(self, content_id: str):
        """Increment content view count"""
        try:
            self.content_collection.update_one(
                {"_id": ObjectId(content_id)},
                {"$inc": {"views": 1}}
            )
        except Exception as e:
            print(f"Error updating views: {e}")
    
    # User Progress Management
    def save_user_progress(self, progress_data: Dict[str, Any]) -> str:
        """Save user learning progress"""
        try:
            progress_doc = UserProgressModel.create_progress(**progress_data)
            result = self.progress_collection.insert_one(progress_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving progress: {e}")
            return None
    
    def get_user_progress(self, user_id: str, subject: str = None) -> List[Dict[str, Any]]:
        """Get user's learning progress"""
        try:
            filter_query = {"user_id": user_id}
            if subject:
                filter_query["subject"] = subject.lower()
            
            cursor = self.progress_collection.find(filter_query).sort("timestamp", -1)
            return list(cursor)
        except Exception as e:
            print(f"Error getting progress: {e}")
            return []
    
    def get_user_performance_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive performance summary for user"""
        try:
            pipeline = [
                {"$match": {"user_id": user_id}},
                {"$group": {
                    "_id": "$subject",
                    "total_sessions": {"$sum": 1},
                    "average_score": {"$avg": "$score"},
                    "best_score": {"$max": "$score"},
                    "total_questions": {"$sum": "$total_questions"},
                    "total_correct": {"$sum": "$correct_answers"},
                    "total_time": {"$sum": "$time_spent"}
                }},
                {"$sort": {"average_score": -1}}
            ]
            
            results = list(self.progress_collection.aggregate(pipeline))
            return results
        except Exception as e:
            print(f"Error getting performance summary: {e}")
            return []
    
    # Question Management
    def add_question(self, question_data: Dict[str, Any]) -> str:
        """Add new assessment question"""
        try:
            question_doc = QuestionModel.create_question(**question_data)
            result = self.questions_collection.insert_one(question_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error adding question: {e}")
            return None
    
    def get_questions_by_topic(self, subject: str, topic: str, difficulty: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get questions by topic and difficulty"""
        try:
            filter_query = {
                "subject": subject.lower(),
                "topic": topic.lower()
            }
            if difficulty:
                filter_query["difficulty"] = difficulty.lower()
            
            cursor = self.questions_collection.find(filter_query).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error getting questions: {e}")
            return []
    
    def update_question_stats(self, question_id: str, is_correct: bool, time_taken: int):
        """Update question usage statistics"""
        try:
            update_data = {
                "$inc": {
                    "usage_count": 1,
                    "total_time": time_taken
                }
            }
            
            if is_correct:
                update_data["$inc"]["correct_count"] = 1
            
            self.questions_collection.update_one(
                {"_id": ObjectId(question_id)},
                update_data
            )
            
            # Update success rate
            question = self.questions_collection.find_one({"_id": ObjectId(question_id)})
            if question and question.get("usage_count", 0) > 0:
                success_rate = question.get("correct_count", 0) / question["usage_count"]
                self.questions_collection.update_one(
                    {"_id": ObjectId(question_id)},
                    {"$set": {"success_rate": success_rate}}
                )
                
        except Exception as e:
            print(f"Error updating question stats: {e}")
    
    # User Management
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create new user account"""
        try:
            user_doc = UserModel.create_user(**user_data)
            result = self.users_collection.insert_one(user_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            return self.users_collection.find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user learning preferences"""
        try:
            self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"learning_preferences": preferences}}
            )
        except Exception as e:
            print(f"Error updating preferences: {e}")
    
    # Study Session Management
    def start_study_session(self, session_data: Dict[str, Any]) -> str:
        """Start a new study session"""
        try:
            session_doc = StudySessionModel.create_session(**session_data)
            result = self.sessions_collection.insert_one(session_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error starting session: {e}")
            return None
    
    def end_study_session(self, session_id: str, final_score: float, duration: int):
        """End a study session"""
        try:
            update_data = StudySessionModel.end_session(session_id, final_score, duration)
            self.sessions_collection.update_one(
                {"_id": ObjectId(session_id)},
                update_data
            )
        except Exception as e:
            print(f"Error ending session: {e}")
    
    def get_user_sessions(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's study sessions"""
        try:
            cursor = self.sessions_collection.find(
                {"user_id": user_id}
            ).sort("start_time", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []
    
    # Analytics and Reporting
    def get_subject_analytics(self, subject: str) -> Dict[str, Any]:
        """Get analytics for a specific subject"""
        try:
            pipeline = [
                {"$match": {"subject": subject.lower()}},
                {"$group": {
                    "_id": "$topic",
                    "total_sessions": {"$sum": 1},
                    "average_score": {"$avg": "$score"},
                    "total_users": {"$addToSet": "$user_id"}
                }},
                {"$project": {
                    "topic": "$_id",
                    "total_sessions": 1,
                    "average_score": {"$round": ["$average_score", 2]},
                    "unique_users": {"$size": "$total_users"}
                }}
            ]
            
            results = list(self.progress_collection.aggregate(pipeline))
            return results
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return []
    
    def get_daily_activity(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get daily activity for the last N days"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            pipeline = [
                {"$match": {"timestamp": {"$gte": start_date}}},
                {"$group": {
                    "_id": {
                        "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                        "subject": "$subject"
                    },
                    "total_sessions": {"$sum": 1},
                    "average_score": {"$avg": "$score"}
                }},
                {"$sort": {"_id.date": 1}}
            ]
            
            results = list(self.progress_collection.aggregate(pipeline))
            return results
        except Exception as e:
            print(f"Error getting daily activity: {e}")
            return []
    
    # Database Maintenance
    def create_text_indexes(self):
        """Create text search indexes"""
        try:
            # Create text index on content
            self.content_collection.create_index([
                ("title", "text"),
                ("content", "text"),
                ("key_concepts", "text")
            ])
            
            # Create text index on questions
            self.questions_collection.create_index([
                ("question", "text"),
                ("explanation", "text"),
                ("key_points", "text")
            ])
            
            print("✅ Text indexes created successfully")
        except Exception as e:
            print(f"❌ Error creating text indexes: {e}")
    
    def cleanup_old_sessions(self, days_old: int = 30):
        """Clean up old completed study sessions"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            result = self.sessions_collection.delete_many({
                "status": "completed",
                "end_time": {"$lt": cutoff_date}
            })
            print(f"✅ Cleaned up {result.deleted_count} old sessions")
        except Exception as e:
            print(f"❌ Error cleaning up sessions: {e}")

# Global MongoDB service instance
mongodb_service = MongoDBService()
