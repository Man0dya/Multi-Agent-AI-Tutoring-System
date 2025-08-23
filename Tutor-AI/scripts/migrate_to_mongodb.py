#!/usr/bin/env python3
"""
Migration script to move from in-memory storage to MongoDB
Run this script to populate MongoDB with initial educational content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.mongodb_config import mongodb_config
from services.mongodb_service import mongodb_service
from datetime import datetime

def migrate_educational_content():
    """Migrate built-in educational content to MongoDB"""
    print("🚀 Starting MongoDB migration...")
    
    # Test MongoDB connection
    if not mongodb_config.connect():
        print("❌ Cannot connect to MongoDB. Please ensure MongoDB is running.")
        return False
    
    # Create indexes
    mongodb_config.create_indexes()
    mongodb_service.create_text_indexes()
    
    # Initial educational content
    educational_content = [
        {
            "title": "Python Programming Fundamentals",
            "content": """
            Python is a high-level, interpreted programming language known for its simplicity and readability. 
            It supports multiple programming paradigms including procedural, object-oriented, and functional programming.
            
            Key concepts include:
            - Variables and data types (int, float, string, list, dict)
            - Control structures (if/else, loops, functions)
            - Object-oriented programming (classes, inheritance, polymorphism)
            - File handling and modules
            
            Python is widely used in:
            - Web development (Django, Flask)
            - Data science (NumPy, Pandas, Matplotlib)
            - Artificial intelligence and machine learning
            - Automation and scripting
            """,
            "subject": "computer_science",
            "topic": "python_programming",
            "content_type": "lesson",
            "difficulty": "beginner",
            "learning_objectives": [
                "Understand Python syntax and basic concepts",
                "Write simple Python programs",
                "Use control structures and functions",
                "Work with different data types"
            ],
            "key_concepts": [
                "Variables", "Data Types", "Control Structures", 
                "Functions", "Object-Oriented Programming", "Modules"
            ],
            "tags": ["programming", "python", "beginner", "fundamentals"]
        },
        {
            "title": "Data Structures and Algorithms",
            "content": """
            Data structures are ways of organizing and storing data to enable efficient access and modification.
            Understanding data structures is crucial for writing efficient algorithms.
            
            Common Data Structures:
            1. Arrays: Fixed-size collections with index-based access
            2. Linked Lists: Dynamic collections with pointer-based access
            3. Stacks: LIFO (Last-In-First-Out) data structure
            4. Queues: FIFO (First-In-First-Out) data structure
            5. Trees: Hierarchical structures for searching and sorting
            6. Hash Tables: Key-value pairs with average O(1) access
            
            Algorithm Analysis:
            - Time complexity using Big O notation
            - Space complexity considerations
            - Best, worst, and average case scenarios
            """,
            "subject": "computer_science",
            "topic": "data_structures",
            "content_type": "lesson",
            "difficulty": "intermediate",
            "learning_objectives": [
                "Understand different data structure types",
                "Analyze time and space complexity",
                "Implement basic data structures",
                "Choose appropriate structures for problems"
            ],
            "key_concepts": [
                "Arrays", "Linked Lists", "Stacks", "Queues", 
                "Trees", "Hash Tables", "Complexity Analysis"
            ],
            "tags": ["data structures", "algorithms", "complexity", "computer science"]
        },
        {
            "title": "Calculus Fundamentals",
            "content": """
            Calculus is the mathematical study of continuous change and motion.
            It provides tools for understanding rates of change and accumulation.
            
            Differential Calculus:
            - Derivatives measure rates of change
            - Rules for finding derivatives (power rule, chain rule, product rule)
            - Applications in optimization and physics
            
            Integral Calculus:
            - Integrals measure accumulation of quantities
            - Definite and indefinite integrals
            - Techniques: substitution, integration by parts
            
            Applications:
            - Physics: motion, forces, energy
            - Economics: marginal analysis, optimization
            - Engineering: design optimization, control systems
            """,
            "subject": "mathematics",
            "topic": "calculus",
            "content_type": "lesson",
            "difficulty": "advanced",
            "learning_objectives": [
                "Understand the concept of derivatives and integrals",
                "Apply differentiation and integration rules",
                "Solve optimization problems",
                "Apply calculus to real-world problems"
            ],
            "key_concepts": [
                "Derivatives", "Integrals", "Limits", "Continuity",
                "Optimization", "Applications"
            ],
            "tags": ["calculus", "mathematics", "derivatives", "integrals", "optimization"]
        }
    ]
    
    # Migrate content
    migrated_count = 0
    for content in educational_content:
        try:
            content_id = mongodb_service.add_content(content)
            if content_id:
                migrated_count += 1
                print(f"✅ Migrated: {content['title']}")
            else:
                print(f"❌ Failed to migrate: {content['title']}")
        except Exception as e:
            print(f"❌ Error migrating {content['title']}: {e}")
    
    print(f"\n🎉 Migration completed! {migrated_count}/{len(educational_content)} content items migrated.")
    return True

def create_sample_questions():
    """Create sample assessment questions"""
    print("\n📝 Creating sample questions...")
    
    sample_questions = [
        {
            "question": "What is the time complexity of accessing an element in an array?",
            "question_type": "multiple_choice",
            "subject": "computer_science",
            "topic": "data_structures",
            "difficulty": "easy",
            "bloom_level": "remember",
            "correct_answer": "O(1)",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "explanation": "Array access is constant time O(1) because we can directly calculate the memory address using the index.",
            "key_points": ["Array access", "Time complexity", "Constant time"],
            "tags": ["arrays", "complexity", "data structures"]
        },
        {
            "question": "Which of the following is NOT a valid Python data type?",
            "question_type": "multiple_choice",
            "subject": "computer_science",
            "topic": "python_programming",
            "difficulty": "easy",
            "bloom_level": "remember",
            "correct_answer": "char",
            "options": ["int", "float", "char", "list"],
            "explanation": "Python doesn't have a 'char' type. Single characters are represented as strings of length 1.",
            "key_points": ["Python data types", "Character representation", "String type"],
            "tags": ["python", "data types", "beginner"]
        },
        {
            "question": "What is the derivative of x²?",
            "question_type": "multiple_choice",
            "subject": "mathematics",
            "topic": "calculus",
            "difficulty": "medium",
            "bloom_level": "apply",
            "correct_answer": "2x",
            "options": ["x", "2x", "x²", "2x²"],
            "explanation": "Using the power rule: d/dx(x^n) = n*x^(n-1). So d/dx(x²) = 2*x^(2-1) = 2x.",
            "key_points": ["Power rule", "Derivative", "Polynomial"],
            "tags": ["calculus", "derivatives", "power rule"]
        }
    ]
    
    questions_created = 0
    for question in sample_questions:
        try:
            question_id = mongodb_service.add_question(question)
            if question_id:
                questions_created += 1
                print(f"✅ Created question: {question['question'][:50]}...")
            else:
                print(f"❌ Failed to create question")
        except Exception as e:
            print(f"❌ Error creating question: {e}")
    
    print(f"📊 {questions_created}/{len(sample_questions)} sample questions created.")
    return questions_created

def main():
    """Main migration function"""
    print("=" * 60)
    print("🎓 AI Tutoring System - MongoDB Migration")
    print("=" * 60)
    
    try:
        # Migrate educational content
        if migrate_educational_content():
            # Create sample questions
            create_sample_questions()
            
            # Show database stats
            stats = mongodb_config.get_stats()
            print(f"\n📊 Database Statistics:")
            print(f"Database: {stats.get('database', 'Unknown')}")
            print(f"Collections: {stats.get('collections', 0)}")
            print(f"Collections: {', '.join(stats.get('collection_names', []))}")
            
            print("\n✅ Migration completed successfully!")
            print("🚀 Your AI Tutoring System is now using MongoDB!")
            
        else:
            print("❌ Migration failed. Please check MongoDB connection.")
            
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    finally:
        # Close MongoDB connection
        mongodb_config.close_connection()
    
    return True

if __name__ == "__main__":
    main()
