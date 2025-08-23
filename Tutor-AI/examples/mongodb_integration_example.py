#!/usr/bin/env python3
"""
Example of how to integrate MongoDB with the AI Tutoring System
This shows how to replace in-memory storage with MongoDB
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.mongodb_service import mongodb_service
from config.mongodb_config import mongodb_config

def example_content_management():
    """Example of content management with MongoDB"""
    print("📚 Content Management Example")
    print("-" * 40)
    
    # Add new educational content
    new_content = {
        "title": "Machine Learning Basics",
        "content": """
        Machine Learning is a subset of artificial intelligence that enables computers to learn 
        and improve from experience without being explicitly programmed.
        
        Key Concepts:
        - Supervised Learning: Learning from labeled data
        - Unsupervised Learning: Finding patterns in unlabeled data
        - Reinforcement Learning: Learning through interaction with environment
        
        Common Algorithms:
        - Linear Regression
        - Decision Trees
        - Neural Networks
        - Support Vector Machines
        """,
        "subject": "computer_science",
        "topic": "machine_learning",
        "content_type": "lesson",
        "difficulty": "intermediate",
        "learning_objectives": [
            "Understand basic ML concepts",
            "Identify different learning types",
            "Recognize common algorithms"
        ],
        "key_concepts": [
            "Supervised Learning", "Unsupervised Learning", 
            "Reinforcement Learning", "Algorithms"
        ],
        "tags": ["machine learning", "AI", "algorithms", "data science"]
    }
    
    # Save to MongoDB
    content_id = mongodb_service.add_content(new_content)
    if content_id:
        print(f"✅ Content saved with ID: {content_id}")
        
        # Retrieve content
        content = mongodb_service.get_content_by_subject("computer_science", limit=5)
        print(f"📖 Retrieved {len(content)} computer science lessons")
        
        # Search content
        search_results = mongodb_service.search_content("machine learning")
        print(f"🔍 Found {len(search_results)} results for 'machine learning'")
        
    else:
        print("❌ Failed to save content")

def example_user_progress():
    """Example of user progress tracking with MongoDB"""
    print("\n👤 User Progress Tracking Example")
    print("-" * 40)
    
    # Create a user (in real app, this would be from authentication)
    user_data = {
        "username": "student123",
        "email": "student@example.com",
        "learning_preferences": {
            "difficulty_preference": "medium",
            "preferred_subjects": ["computer_science", "mathematics"],
            "learning_style": "visual",
            "daily_goal": 45
        },
        "subjects_of_interest": ["computer_science", "mathematics"]
    }
    
    user_id = mongodb_service.create_user(user_data)
    if user_id:
        print(f"✅ User created with ID: {user_id}")
        
        # Save user progress
        progress_data = {
            "user_id": user_id,
            "subject": "computer_science",
            "topic": "python_programming",
            "score": 85.5,
            "total_questions": 10,
            "correct_answers": 8,
            "time_spent": 1200,  # seconds
            "difficulty": "medium"
        }
        
        progress_id = mongodb_service.save_user_progress(progress_data)
        if progress_id:
            print(f"✅ Progress saved with ID: {progress_id}")
            
            # Get user performance summary
            performance = mongodb_service.get_user_performance_summary(user_id)
            print(f"📊 Performance summary: {len(performance)} subjects")
            
            for subject_perf in performance:
                print(f"  {subject_perf['_id']}: {subject_perf['average_score']:.1f}% avg")
        else:
            print("❌ Failed to save progress")
    else:
        print("❌ Failed to create user")

def example_question_management():
    """Example of question management with MongoDB"""
    print("\n❓ Question Management Example")
    print("-" * 40)
    
    # Add a new question
    new_question = {
        "question": "What is the time complexity of binary search?",
        "question_type": "multiple_choice",
        "subject": "computer_science",
        "topic": "algorithms",
        "difficulty": "medium",
        "bloom_level": "understand",
        "correct_answer": "O(log n)",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
        "explanation": "Binary search divides the search space in half with each iteration, resulting in logarithmic time complexity.",
        "key_points": ["Binary search", "Time complexity", "Logarithmic"],
        "tags": ["algorithms", "search", "complexity", "binary search"]
    }
    
    question_id = mongodb_service.add_question(new_question)
    if question_id:
        print(f"✅ Question saved with ID: {question_id}")
        
        # Get questions by topic
        questions = mongodb_service.get_questions_by_topic(
            subject="computer_science",
            topic="algorithms",
            difficulty="medium",
            limit=5
        )
        print(f"📝 Retrieved {len(questions)} algorithm questions")
        
        # Update question statistics (simulate user answering)
        mongodb_service.update_question_stats(question_id, is_correct=True, time_taken=45)
        print("📊 Question statistics updated")
        
    else:
        print("❌ Failed to save question")

def example_study_sessions():
    """Example of study session management with MongoDB"""
    print("\n⏱️ Study Session Management Example")
    print("-" * 40)
    
    # Start a study session
    session_data = {
        "user_id": "demo_user_123",
        "subject": "mathematics",
        "topic": "calculus",
        "session_type": "practice"
    }
    
    session_id = mongodb_service.start_study_session(session_data)
    if session_id:
        print(f"✅ Study session started with ID: {session_id}")
        
        # End the session (simulate completion)
        mongodb_service.end_study_session(session_id, final_score=78.5, duration=1800)
        print("✅ Study session completed")
        
        # Get user sessions
        sessions = mongodb_service.get_user_sessions("demo_user_123", limit=5)
        print(f"📚 Retrieved {len(sessions)} study sessions")
        
    else:
        print("❌ Failed to start study session")

def example_analytics():
    """Example of analytics and reporting with MongoDB"""
    print("\n📊 Analytics and Reporting Example")
    print("-" * 40)
    
    # Get subject analytics
    cs_analytics = mongodb_service.get_subject_analytics("computer_science")
    print(f"💻 Computer Science Analytics: {len(cs_analytics)} topics")
    
    for topic_analytics in cs_analytics:
        print(f"  {topic_analytics['topic']}: {topic_analytics['average_score']:.1f}% avg")
    
    # Get daily activity
    daily_activity = mongodb_service.get_daily_activity(days=7)
    print(f"📅 Daily Activity: {len(daily_activity)} days of data")
    
    # Database statistics
    stats = mongodb_config.get_stats()
    print(f"\n🗄️ Database Statistics:")
    print(f"  Database: {stats.get('database', 'Unknown')}")
    print(f"  Collections: {stats.get('collections', 0)}")
    print(f"  Collections: {', '.join(stats.get('collection_names', []))}")

def main():
    """Run all MongoDB integration examples"""
    print("🚀 MongoDB Integration Examples")
    print("=" * 50)
    
    # Test MongoDB connection
    if not mongodb_config.connect():
        print("❌ Cannot connect to MongoDB. Please ensure MongoDB is running.")
        print("\n💡 To install MongoDB locally:")
        print("   1. Download from: https://www.mongodb.com/try/download/community")
        print("   2. Install and start MongoDB service")
        print("   3. Or use MongoDB Atlas (cloud): https://www.mongodb.com/atlas")
        return False
    
    try:
        # Run examples
        example_content_management()
        example_user_progress()
        example_question_management()
        example_study_sessions()
        example_analytics()
        
        print("\n🎉 All examples completed successfully!")
        print("🚀 Your AI Tutoring System is now using MongoDB!")
        
    except Exception as e:
        print(f"❌ Example error: {e}")
        return False
    
    finally:
        # Close MongoDB connection
        mongodb_config.close_connection()
    
    return True

if __name__ == "__main__":
    main()
