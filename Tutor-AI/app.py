from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from agents.content_generator import ContentGeneratorAgent
from agents.question_setter import QuestionSetterAgent
from agents.feedback_evaluator import FeedbackEvaluatorAgent
from database.mongodb_session_manager import MongoDBSessionManager
from utils.security import SecurityManager

# Configure page
st.set_page_config(
    page_title="AI Tutoring System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("styles/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = MongoDBSessionManager()
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Initialize agents
@st.cache_resource
def initialize_agents():
    content_agent = ContentGeneratorAgent()
    question_agent = QuestionSetterAgent()
    feedback_agent = FeedbackEvaluatorAgent()
    return content_agent, question_agent, feedback_agent

content_agent, question_agent, feedback_agent = initialize_agents()

# Security manager
security = SecurityManager()

def authenticate_user():
    """Simple authentication interface"""
    st.sidebar.title("🔐 Authentication")
    
    if st.session_state.current_user is None:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            # Basic authentication (in production, use proper authentication)
            if username and password:
                sanitized_username = security.sanitize_input(username)
                st.session_state.current_user = sanitized_username
                st.sidebar.success(f"Welcome, {sanitized_username}!")
                st.rerun()
            else:
                st.sidebar.error("Please enter valid credentials")
    else:
        st.sidebar.success(f"Logged in as: {st.session_state.current_user}")
        if st.sidebar.button("Logout"):
            st.session_state.current_user = None
            st.rerun()

def main_interface():
    """Main tutoring interface"""
    
    # Header
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.title("🎓 AI Tutoring System")
    
    with col2:
        st.markdown("### Multi-Agent Educational Platform")
    
    with col3:
        # Dark mode toggle
        if st.button("🌓 Toggle Theme"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Content Generator", 
        "❓ Question Setter", 
        "✅ Feedback Evaluator", 
        "📊 Progress Tracking",
        "🔍 Knowledge Base"
    ])
    
    with tab1:
        content_generator_interface()
    
    with tab2:
        question_setter_interface()
    
    with tab3:
        feedback_evaluator_interface()
    
    with tab4:
        progress_tracking_interface()
    
    with tab5:
        knowledge_base_interface()
    
    # Add adaptive learning workflow as a separate section
    if st.sidebar.button("🔄 Adaptive Learning Workflow", use_container_width=True):
        st.session_state.active_tab = "adaptive"
        st.rerun()
    
    if st.session_state.get('active_tab') == "adaptive":
        adaptive_learning_interface()

def content_generator_interface():
    """Enhanced Content Generator Agent Interface - Teacher Role"""
    st.header("👨‍🏫 Content Generator Agent (Teacher)")
    st.markdown("**Teacher Role**: Creates comprehensive, student-friendly study materials with reliable sources and key concept extraction.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("📖 Enter Topic", placeholder="e.g., Photosynthesis, Machine Learning, World War II")
        
        learning_objectives = st.text_area(
            "🎯 Learning Objectives (Optional)",
            placeholder="What should students understand after studying this topic?",
            height=80
        )
    
    with col2:
        difficulty = st.select_slider("📊 Difficulty Level", 
                                    options=["Beginner", "Intermediate", "Advanced"])
        
        subject = st.selectbox("🎯 Subject Area", [
            "Science", "Mathematics", "Computer Science", "History", 
            "Literature", "Languages", "Business", "Arts", "General"
        ])
        
        content_type = st.selectbox("📋 Content Type", [
            "Study Notes", "Tutorial", "Explanation", "Summary", "Comprehensive Guide"
        ])
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        include_flashcards = st.checkbox("Generate Flashcards", value=True)
        include_diagrams = st.checkbox("Suggest Diagrams", value=True)
        source_quality = st.selectbox(
            "Source Preference",
            options=["Academic & Educational", "Academic Only", "Educational Only"]
        )
    
    if st.button("🚀 Generate Study Materials", type="primary"):
        if topic:
            with st.spinner("👨‍🏫 Teacher is creating comprehensive study materials..."):
                try:
                    # Sanitize input
                    clean_topic = security.sanitize_input(topic)
                    
                    # Parse learning objectives
                    objectives = [obj.strip() for obj in learning_objectives.split('\n') if obj.strip()] if learning_objectives else None
                    
                    # Generate enhanced content using updated agent
                    content_result = content_agent.generate_content(
                        topic=clean_topic,
                        difficulty=difficulty,
                        subject=subject,
                        content_type=content_type,
                        learning_objectives=objectives
                    )
                    
                    st.success("✅ Study materials created successfully!")
                    
                    # Handle both old and new content format
                    if isinstance(content_result, dict):
                        main_content = content_result.get('content', str(content_result))
                        study_materials = content_result.get('study_materials', {})
                        key_concepts = content_result.get('key_concepts', [])
                        objectives_list = content_result.get('learning_objectives', objectives or [])
                        source_quality_score = content_result.get('sources', {}).get('quality_score', 0.5)
                    else:
                        # Fallback for old format
                        main_content = content_result
                        study_materials = {}
                        key_concepts = []
                        objectives_list = objectives or []
                        source_quality_score = 0.5
                    
                    # Display main content
                    with st.expander("📖 Study Notes", expanded=True):
                        st.markdown(main_content)
                    
                    # Display study materials in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Key Concepts", "📚 Flashcards", "📊 Learning Objectives", "🎨 Study Aids"])
                    
                    with tab1:
                        st.markdown("#### 🔑 Key Concepts Identified")
                        if key_concepts:
                            for i, concept in enumerate(key_concepts[:10], 1):
                                st.markdown(f"{i}. **{concept}**")
                        else:
                            st.info("Key concepts will be extracted from the content")
                    
                    with tab2:
                        if include_flashcards:
                            st.markdown("#### 🃏 Generated Flashcards")
                            flashcards = study_materials.get('flashcards', [])
                            if flashcards:
                                for i, card in enumerate(flashcards[:8]):
                                    with st.expander(f"Flashcard {i+1}: {card.get('term', f'Concept {i+1}')}"):
                                        st.markdown(f"**Definition:** {card.get('definition', 'Key concept in the topic')}")
                                        st.markdown(f"**Category:** {card.get('category', 'CONCEPT')}")
                            else:
                                st.info("Flashcards will be generated based on key concepts")
                    
                    with tab3:
                        st.markdown("#### 📚 Learning Objectives")
                        if objectives_list:
                            for i, obj in enumerate(objectives_list, 1):
                                st.markdown(f"{i}. {obj}")
                        else:
                            st.info("Learning objectives will be created based on the topic")
                    
                    with tab4:
                        if include_diagrams:
                            st.markdown("#### 🎨 Suggested Diagrams")
                            diagram_suggestions = study_materials.get('diagram_suggestions', [])
                            if diagram_suggestions:
                                for diagram in diagram_suggestions:
                                    st.markdown(f"• **{diagram}** - Recommended for visual learning")
                            else:
                                st.info("Diagram suggestions will be provided based on topic analysis")
                        
                        st.markdown("#### 📝 Study Notes Summary")
                        bullet_notes = study_materials.get('study_notes', '')
                        if bullet_notes:
                            st.markdown(bullet_notes)
                        else:
                            st.info("Study notes summary will be created from main content")
                    
                    # Source quality indicator
                    quality_color = "🟢" if source_quality_score > 0.7 else "🟡" if source_quality_score > 0.4 else "🔴"
                    st.markdown(f"**Source Quality:** {quality_color} {source_quality_score:.1%}")
                    
                    # Save enhanced content to session
                    st.session_state.session_manager.save_content(
                        user=st.session_state.current_user,
                        topic=clean_topic,
                        content=main_content,
                        metadata={
                            "difficulty": difficulty,
                            "subject": subject,
                            "content_type": content_type,
                            "key_concepts": key_concepts,
                            "learning_objectives": objectives_list,
                            "source_quality": source_quality_score,
                            "timestamp": datetime.now().isoformat()
                        }
                    )
                    
                    # Store in session state for workflow continuation
                    st.session_state.last_generated_content = content_result
                    st.session_state.last_content_topic = clean_topic
                    
                    # Quick action to continue workflow
                    st.markdown("### 🔄 Continue Learning Workflow")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("➡️ Generate Questions", type="secondary"):
                            st.switch_page("Question Setter")
                    with col2:
                        if st.button("📋 View Study Sessions", type="secondary"):
                            st.switch_page("Study Sessions")
                    
                except Exception as e:
                    st.error(f"❌ Error generating content: {str(e)}")
                    st.info("The system will fall back to basic content generation if enhanced features aren't available.")
        else:
            st.warning("⚠️ Please enter a topic to generate educational material.")

def question_setter_interface():
    """Enhanced Question Setter Agent Interface - Exam Designer Role"""
    st.header("📝 Question Setter Agent (Exam Designer)")
    st.markdown("**Exam Designer Role**: Creates MCQs, T/F, and short answer questions using Bloom's taxonomy with intelligent difficulty tuning and plausible distractors.")
    
    # Check if quiz is already generated and show it
    if st.session_state.get('show_quiz') and st.session_state.get('quiz_questions'):
        st.info("🎯 Quiz is ready! Answer the questions below.")
        
        # Add reset button
        col1, col2 = st.columns([3, 1])
        with col1:
            display_quiz_interface(st.session_state.quiz_questions)
        with col2:
            if st.button("🔄 Generate New Questions", type="secondary"):
                st.session_state.show_quiz = False
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_completed = False
                st.rerun()
        return
    
    # Get recent content from session
    recent_content = st.session_state.session_manager.get_recent_content(
        st.session_state.current_user
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if recent_content:
            selected_content = st.selectbox(
                "📚 Select Content for Questions",
                options=list(recent_content.keys()),
                format_func=lambda x: f"{x[:50]}..." if len(x) > 50 else x
            )
        else:
            st.info("📝 Generate some content first to create questions.")
            selected_content = None
        
        custom_content = st.text_area(
            "📝 Or Enter Custom Content",
            height=150,
            placeholder="Paste or enter the content you want to generate questions from..."
        )
    
    with col2:
        question_count = st.number_input("🔢 Number of Questions", min_value=1, max_value=20, value=5)
        question_types = st.multiselect(
            "❓ Question Types",
            ["Multiple Choice", "True/False", "Short Answer", "Essay", "Fill in the Blank"],
            default=["Multiple Choice", "Short Answer"]
        )
    
    # Enhanced Bloom's Taxonomy and Difficulty Controls
    with st.expander("🎯 Advanced Question Settings"):
        col1_exp, col2_exp = st.columns(2)
        
        with col1_exp:
            st.markdown("**📚 Bloom's Taxonomy Levels**")
            bloom_levels = st.multiselect(
                "Select Learning Levels",
                ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"],
                default=["Remember", "Understand", "Apply", "Analyze"],
                help="Target specific cognitive learning levels"
            )
        
        with col2_exp:
            st.markdown("**⚖️ Difficulty Distribution**")
            easy_pct = st.slider("Easy %", 0, 100, 30)
            medium_pct = st.slider("Medium %", 0, 100, 50)
            hard_pct = 100 - easy_pct - medium_pct
            st.write(f"Hard: {hard_pct}%")
            
            difficulty_distribution = {
                "Easy": easy_pct / 100,
                "Medium": medium_pct / 100,
                "Hard": hard_pct / 100
            }
        
        generate_distractors = st.checkbox("Generate Smart Distractors for MCQ", value=True)
        adaptive_difficulty = st.checkbox("Adaptive Difficulty Based on Performance", value=True)
    
    if st.button("🎯 Generate Questions", type="primary"):
        content_to_use = None
        
        if custom_content:
            content_to_use = security.sanitize_input(custom_content)
        elif selected_content and recent_content:
            content_to_use = recent_content[selected_content]
        
        if content_to_use:
            with st.spinner("🤖 AI is generating questions..."):
                try:
                    # Get enhanced content if available
                    if hasattr(st.session_state, 'last_generated_content') and isinstance(st.session_state.last_generated_content, dict):
                        content_input = st.session_state.last_generated_content
                    else:
                        content_input = content_to_use
                    
                    # Generate questions with enhanced parameters
                    questions_result = question_agent.generate_questions(
                        content=content_input,
                        question_count=question_count,
                        question_types=question_types,
                        difficulty_distribution=difficulty_distribution if 'difficulty_distribution' in locals() else None,
                        bloom_levels=bloom_levels if 'bloom_levels' in locals() else None
                    )
                    
                    st.success("✅ Questions generated successfully!")
                    
                    # Handle both old and new question format
                    if isinstance(questions_result, dict):
                        questions = questions_result.get('questions', [])
                        metadata = questions_result.get('metadata', {})
                        
                        # Display metadata summary
                        if metadata:
                            st.markdown("### 📊 Question Bank Summary")
                            col1_meta, col2_meta, col3_meta = st.columns(3)
                            
                            with col1_meta:
                                st.metric("Total Questions", metadata.get('total_count', len(questions)))
                                
                            with col2_meta:
                                difficulty_dist = metadata.get('difficulty_distribution', {})
                                if difficulty_dist:
                                    st.write("**Difficulty Mix:**")
                                    for diff, pct in difficulty_dist.items():
                                        st.write(f"• {diff}: {pct:.1%}")
                            
                            with col3_meta:
                                bloom_levels_used = metadata.get('bloom_levels', [])
                                if bloom_levels_used:
                                    st.write("**Bloom Levels:**")
                                    for level in bloom_levels_used[:3]:
                                        st.write(f"• {level}")
                    else:
                        questions = questions_result
                        metadata = {}
                    
                    # Store questions for quiz (without revealing answers)
                    # Flatten the questions structure for easier handling
                    if isinstance(questions, list):
                        quiz_questions = questions
                    else:
                        # Handle case where questions might be nested
                        quiz_questions = questions.get('questions', []) if isinstance(questions, dict) else []
                    
                    st.session_state.quiz_questions = quiz_questions
                    st.session_state.quiz_metadata = metadata
                    
                    st.success("✅ Questions generated! Now take the quiz below.")
                    
                    # Store quiz data and show quiz interface
                    st.session_state.quiz_questions = quiz_questions
                    st.session_state.quiz_topic = selected_content or "Custom Content"
                    st.session_state.show_quiz = True
                    
                    # Show quiz interface
                    display_quiz_interface(quiz_questions)
                    
                    # Save questions to session state for adaptive workflow
                    st.session_state.last_generated_questions = questions_result
                    st.session_state.last_questions_metadata = metadata
                    
                    # Save questions
                    st.session_state.session_manager.save_questions(
                        user=st.session_state.current_user,
                        questions=questions,
                        content_source=selected_content or "Custom Content"
                    )
                    
                    # Continue workflow
                    st.markdown("### 🔄 Continue Learning Workflow")
                    col1_workflow, col2_workflow = st.columns(2)
                    with col1_workflow:
                        if st.button("📊 Go to Feedback Evaluator", type="secondary"):
                            st.session_state.active_tab = "feedback"
                            st.rerun()
                    with col2_workflow:
                        if st.button("📈 View Progress Tracking", type="secondary"):
                            st.session_state.active_tab = "progress"
                            st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating questions: {str(e)}")
        else:
            st.warning("⚠️ Please select content or enter custom content to generate questions.")

def display_quiz_interface(questions):
    """Display the quiz interface with proper state management"""
    st.markdown("---")
    st.markdown("## 📝 Take the Quiz")
    st.markdown("Answer the questions below. Your answers will be evaluated by the AI.")
    
    # Initialize quiz state if not exists
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    
    # Quiz questions interface
    for i, question in enumerate(questions, 1):
        st.markdown(f"---")
        
        # Question header with metadata
        difficulty_badge = ""
        bloom_badge = ""
        
        if question.get('difficulty'):
            diff_color = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}.get(question['difficulty'], "⚪")
            difficulty_badge = f"{diff_color} {question['difficulty']}"
        
        if question.get('bloom_level'):
            bloom_badge = f"📚 {question['bloom_level']}"
        
        st.markdown(f"**Question {i}** {difficulty_badge} {bloom_badge}")
        st.markdown(f"**{question.get('type', 'Question')}**")
        
        # Display question text
        st.markdown(f"**{question['question']}**")
        
        # Answer interface based on question type
        if question['type'] == 'Multiple Choice':
            options = question.get('options', [])
            if options:
                # Use a unique key for each question to prevent conflicts
                answer = st.radio(
                    f"Select your answer:",
                    options,
                    key=f"quiz_q_{st.session_state.get('quiz_topic', 'default')}_{i}",
                    label_visibility="collapsed",
                    index=None  # Start with no selection
                )
                if answer:
                    st.session_state.quiz_answers[i] = answer
            else:
                st.warning("⚠️ No options available for this question")
                st.session_state.quiz_answers[i] = ""
        
        elif question['type'] == 'True/False':
            answer = st.radio(
                f"Select your answer:",
                ["True", "False"],
                key=f"quiz_q_{st.session_state.get('quiz_topic', 'default')}_{i}",
                label_visibility="collapsed",
                index=None  # Start with no selection
            )
            if answer:
                st.session_state.quiz_answers[i] = answer
        
        elif question['type'] in ['Short Answer', 'Essay']:
            answer = st.text_area(
                f"Your answer:",
                key=f"quiz_q_{st.session_state.get('quiz_topic', 'default')}_{i}",
                label_visibility="collapsed",
                height=100,
                placeholder="Type your answer here..."
            )
            if answer:
                st.session_state.quiz_answers[i] = answer
        
        elif question['type'] == 'Fill in the Blank':
            answer = st.text_input(
                f"Your answer:",
                key=f"quiz_q_{st.session_state.get('quiz_topic', 'default')}_{i}",
                label_visibility="collapsed",
                placeholder="Fill in the blank..."
            )
            if answer:
                st.session_state.quiz_answers[i] = answer
    
    # Submit quiz button
    if st.button("📊 Submit Quiz & Get Feedback", type="primary", use_container_width=True):
        if len(st.session_state.quiz_answers) == len(questions):
            st.session_state.quiz_completed = True
            st.success("✅ Quiz submitted! Redirecting to Feedback Evaluator...")
            st.rerun()
        else:
            st.warning("⚠️ Please answer all questions before submitting.")
    
    # Show answer count
    answered_count = len([ans for ans in st.session_state.quiz_answers.values() if ans])
    st.info(f"📝 You have answered {answered_count}/{len(questions)} questions")

def adaptive_learning_interface():
    """Adaptive Learning Workflow - Complete learning loop with difficulty adjustment"""
    st.header("🔄 Adaptive Learning Workflow")
    st.markdown("**Complete Learning Loop**: Adaptive system that adjusts difficulty and focus areas based on your performance.")
    
    # Check if we have content and questions
    if not hasattr(st.session_state, 'last_generated_content'):
        st.info("Start by generating content in the Content Generator to begin the adaptive learning workflow.")
        if st.button("🚀 Go to Content Generator"):
            st.session_state.active_tab = None
            st.rerun()
        return
    
    # Current learning state
    st.markdown("### 🎯 Current Learning State")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_topic = getattr(st.session_state, 'last_content_topic', 'Unknown Topic')
        st.metric("📚 Current Topic", current_topic)
    
    with col2:
        questions_available = len(getattr(st.session_state, 'last_generated_questions', {}).get('questions', []))
        st.metric("❓ Questions Available", questions_available)
    
    with col3:
        performance_history = getattr(st.session_state, 'performance_history', [])
        if performance_history:
            avg_performance = sum(p.get('overall_score', 0) for p in performance_history[-5:]) / len(performance_history[-5:])
        else:
            avg_performance = 0
        st.metric("📊 Recent Avg Score", f"{avg_performance:.1f}%")
    
    # Adaptive recommendations
    st.markdown("### 🤖 AI Recommendations")
    
    # Analyze performance and suggest next steps
    if performance_history:
        latest_performance = performance_history[-1]
        
        if latest_performance.get('overall_score', 0) >= 80:
            st.success("🌟 **Excellent Performance!** Ready for advanced challenges.")
            recommended_difficulty = "Hard"
            recommended_action = "Advance to higher-level concepts or explore related topics"
        elif latest_performance.get('overall_score', 0) >= 60:
            st.info("📈 **Good Progress!** Ready for moderate challenges.")
            recommended_difficulty = "Medium"
            recommended_action = "Continue with current level, add some challenging questions"
        else:
            st.warning("📖 **Need More Practice.** Focus on fundamentals.")
            recommended_difficulty = "Easy"
            recommended_action = "Review basics and practice with easier questions"
        
        st.markdown(f"**Recommended Next Steps:** {recommended_action}")
        st.markdown(f"**Suggested Difficulty:** {recommended_difficulty}")
    else:
        st.info("Take your first quiz to get personalized recommendations!")
    
    # Interactive learning actions
    st.markdown("### 🎮 Learning Actions")
    
    col1_action, col2_action, col3_action = st.columns(3)
    
    with col1_action:
        if st.button("📚 Generate New Content", type="primary"):
            # Adaptive content generation based on performance
            weak_concepts = []
            if performance_history:
                latest = performance_history[-1]
                weak_concepts = latest.get('improvement_areas', [])
            
            st.session_state.adaptive_mode = True
            st.session_state.focus_areas = weak_concepts
            st.success("🔄 Adaptive mode activated! Content will focus on your weak areas.")
    
    with col2_action:
        if st.button("❓ Generate Adaptive Questions", type="secondary"):
            # Adjust question difficulty based on performance
            if performance_history:
                avg_score = sum(p.get('overall_score', 0) for p in performance_history[-3:]) / max(len(performance_history[-3:]), 1)
                
                if avg_score >= 85:
                    difficulty_dist = {"Easy": 0.1, "Medium": 0.4, "Hard": 0.5}
                    bloom_focus = ["Apply", "Analyze", "Evaluate", "Create"]
                elif avg_score >= 70:
                    difficulty_dist = {"Easy": 0.2, "Medium": 0.6, "Hard": 0.2}
                    bloom_focus = ["Understand", "Apply", "Analyze"]
                else:
                    difficulty_dist = {"Easy": 0.5, "Medium": 0.4, "Hard": 0.1}
                    bloom_focus = ["Remember", "Understand", "Apply"]
                
                st.session_state.adaptive_difficulty = difficulty_dist
                st.session_state.adaptive_bloom = bloom_focus
                st.success(f"🎯 Questions will be adapted: {int(difficulty_dist['Hard']*100)}% Hard, {int(difficulty_dist['Medium']*100)}% Medium, {int(difficulty_dist['Easy']*100)}% Easy")
    
    with col3_action:
        if st.button("📋 Take Adaptive Quiz", type="secondary"):
            # Start an adaptive quiz session
            st.session_state.quiz_mode = "adaptive"
            st.info("🚀 Starting adaptive quiz based on your learning profile...")
    
    # Performance analytics
    if performance_history:
        st.markdown("### 📈 Learning Analytics")
        
        # Concept mastery
        st.markdown("#### 🎯 Recent Concept Performance")
        latest_concepts = performance_history[-1].get('concept_scores', {})
        if latest_concepts:
            for concept, score in list(latest_concepts.items())[:5]:
                progress_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                st.markdown(f"{progress_color} **{concept}**: {score:.1f}%")
    
    # Learning path recommendations
    st.markdown("### 🛤️ Suggested Learning Path")
    
    if current_topic and performance_history:
        latest_performance = performance_history[-1]
        strengths = latest_performance.get('strengths', [])
        improvements = latest_performance.get('improvement_areas', [])
        
        if strengths:
            st.markdown("**Build on your strengths:**")
            for strength in strengths[:3]:
                st.markdown(f"• {strength}")
        
        if improvements:
            st.markdown("**Focus areas for improvement:**")
            for improvement in improvements[:3]:
                st.markdown(f"• {improvement}")
    else:
        st.info("Complete a quiz to get personalized learning path recommendations.")

def feedback_evaluator_interface():
    """Feedback Evaluator Agent Interface"""
    st.header("✅ Feedback Evaluator Agent")
    st.markdown("Get personalized feedback on your answers and performance.")
    
    # Check if user has completed a quiz
    if st.session_state.get('quiz_completed') and st.session_state.get('quiz_questions'):
        st.success("🎯 Quiz completed! Here's your personalized feedback.")
        
        # Get quiz data
        questions = st.session_state.quiz_questions
        user_answers = st.session_state.quiz_answers
        quiz_topic = st.session_state.get('quiz_topic', 'Quiz')
        
        # Ensure questions is a list
        if not isinstance(questions, list):
            st.error("❌ Invalid question format. Please regenerate questions.")
            return
        
        st.markdown(f"### 📝 Quiz Results: {quiz_topic}")
        st.markdown(f"**Total Questions:** {len(questions)}")
        st.markdown(f"**Questions Answered:** {len(user_answers)}")
        
        # Evaluate answers using AI
        with st.spinner("🤖 AI is evaluating your answers..."):
            try:
                feedback = feedback_agent.evaluate_answers(
                    questions=questions,
                    user_answers=user_answers,
                    feedback_type="Detailed",
                    include_suggestions=True
                )
                
                st.success("✅ Feedback generated successfully!")
                
                # Display overall score
                col_score1, col_score2, col_score3 = st.columns(3)
                
                with col_score1:
                    st.metric("📊 Overall Score", f"{feedback.get('overall_score', 0)}%")
                
                with col_score2:
                    st.metric("✅ Correct Answers", f"{feedback.get('correct_count', 0)}/{len(questions)}")
                
                with col_score3:
                    performance = "Excellent" if feedback.get('overall_score', 0) >= 80 else "Good" if feedback.get('overall_score', 0) >= 60 else "Needs Improvement"
                    st.metric("🎯 Performance", performance)
                
                # Detailed feedback
                with st.expander("📋 Detailed Feedback", expanded=True):
                    st.markdown(feedback.get('detailed_feedback', ''))
                
                if 'study_suggestions' in feedback:
                    with st.expander("💡 Study Suggestions", expanded=True):
                        st.markdown(feedback['study_suggestions'])
                
                # Save feedback to MongoDB
                st.session_state.session_manager.save_feedback(
                    user=st.session_state.current_user,
                    feedback=feedback,
                    question_set=quiz_topic
                )
                
                # Clear quiz state
                st.session_state.quiz_completed = False
                st.session_state.quiz_questions = None
                st.session_state.quiz_answers = {}
                
                st.info("💡 **Next Step:** Generate new content or questions to continue learning!")
                
            except Exception as e:
                st.error(f"❌ Error evaluating answers: {str(e)}")
        
        return
    
    # Get recent questions from database (fallback)
    recent_questions = st.session_state.session_manager.get_recent_questions(
        st.session_state.current_user
    )
    
    if not recent_questions:
        st.info("📝 Complete a quiz first to receive feedback, or generate questions to take a quiz.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_question_set = st.selectbox(
            "❓ Select Question Set",
            options=list(recent_questions.keys())
        )
        
        if selected_question_set:
            questions_data = recent_questions[selected_question_set]
            
            # Handle different question data structures
            if isinstance(questions_data, dict) and 'questions' in questions_data:
                questions = questions_data['questions']
            elif isinstance(questions_data, list):
                questions = questions_data
            else:
                st.error("❌ Invalid question format in database.")
                return
            
            st.markdown("### 📝 Answer the Questions")
            user_answers = {}
            
            # Initialize variables to avoid unbound errors
            
            for i, question in enumerate(questions):
                # Handle different question structures
                if isinstance(question, dict):
                    question_text = question.get('question', question.get('question_text', 'Question text not available'))
                    question_type = question.get('type', question.get('question_type', 'Unknown'))
                else:
                    question_text = str(question)
                    question_type = 'Unknown'
                
                st.markdown(f"**Question {i+1}:** {question_text}")
                
                if question_type == 'Multiple Choice':
                    options = question.get('options', [])
                    if options:
                        answer = st.radio(
                            f"Select answer for Q{i+1}:",
                            options,
                            key=f"q_{i}",
                            label_visibility="collapsed"
                        )
                        user_answers[i] = answer
                    else:
                        st.warning("⚠️ No options available for this question")
                        user_answers[i] = ""
                
                elif question_type == 'True/False':
                    answer = st.radio(
                        f"Select answer for Q{i+1}:",
                        ["True", "False"],
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    user_answers[i] = answer
                
                elif question_type in ['Short Answer', 'Essay']:
                    answer = st.text_area(
                        f"Your answer for Q{i+1}:",
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    user_answers[i] = security.sanitize_input(answer) if answer else ""
                
                st.markdown("---")
    
    with col2:
        feedback_type = st.selectbox(
            "🎯 Feedback Type",
            ["Detailed", "Summary", "Constructive", "Encouraging"]
        )
        
        include_suggestions = st.checkbox("💡 Include Study Suggestions", value=True)
    
    if st.button("📊 Evaluate & Get Feedback", type="primary"):
        if 'user_answers' in locals() and user_answers and 'questions' in locals() and questions:
            with st.spinner("🤖 AI is evaluating your answers..."):
                try:
                    feedback = feedback_agent.evaluate_answers(
                        questions=questions,
                        user_answers=user_answers,
                        feedback_type=feedback_type,
                        include_suggestions=include_suggestions
                    )
                    
                    st.success("✅ Feedback generated successfully!")
                    
                    # Display overall score
                    col_score1, col_score2, col_score3 = st.columns(3)
                    
                    with col_score1:
                        st.metric("📊 Overall Score", f"{feedback.get('overall_score', 0)}%")
                    
                    with col_score2:
                        total_questions = len(questions) if 'questions' in locals() and questions else 0
                        st.metric("✅ Correct Answers", f"{feedback.get('correct_count', 0)}/{total_questions}")
                    
                    with col_score3:
                        performance = "Excellent" if feedback.get('overall_score', 0) >= 80 else "Good" if feedback.get('overall_score', 0) >= 60 else "Needs Improvement"
                        st.metric("🎯 Performance", performance)
                    
                    # Detailed feedback
                    with st.expander("📋 Detailed Feedback", expanded=True):
                        st.markdown(feedback.get('detailed_feedback', ''))
                    
                    if include_suggestions and 'study_suggestions' in feedback:
                        with st.expander("💡 Study Suggestions", expanded=True):
                            st.markdown(feedback['study_suggestions'])
                    
                    # Save feedback
                    st.session_state.session_manager.save_feedback(
                        user=st.session_state.current_user,
                        feedback=feedback,
                        question_set=selected_question_set
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error evaluating answers: {str(e)}")
        else:
            st.warning("⚠️ Please answer at least one question to get feedback.")

def progress_tracking_interface():
    """Progress Tracking and Analytics Interface"""
    st.header("📊 Progress Tracking & Analytics")
    st.markdown("Monitor your learning progress and performance over time.")
    
    # Get user progress data
    progress_data = st.session_state.session_manager.get_user_progress(
        st.session_state.current_user
    )
    
    if not progress_data:
        st.info("📈 Start learning to see your progress here!")
        return
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Content Generated", progress_data.get('content_count', 0))
    
    with col2:
        st.metric("❓ Questions Answered", progress_data.get('questions_answered', 0))
    
    with col3:
        avg_score = progress_data.get('average_score', 0)
        st.metric("📊 Average Score", f"{avg_score:.1f}%")
    
    with col4:
        study_streak = progress_data.get('study_streak', 0)
        st.metric("🔥 Study Streak", f"{study_streak} days")
    
    # Performance chart
    if 'score_history' in progress_data and progress_data['score_history']:
        st.markdown("### 📈 Performance Over Time")
        
        df = pd.DataFrame(progress_data['score_history'])
        
        fig = px.line(
            df, 
            x='date', 
            y='score',
            title='Score Progression',
            labels={'score': 'Score (%)', 'date': 'Date'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Subject performance
    if 'subject_performance' in progress_data:
        st.markdown("### 🎯 Performance by Subject")
        
        subjects = list(progress_data['subject_performance'].keys())
        scores = list(progress_data['subject_performance'].values())
        
        df_subjects = pd.DataFrame({
            'Subject': subjects,
            'Average Score': scores
        })
        
        fig = px.bar(
            df_subjects,
            x='Subject',
            y='Average Score',
            title='Average Score by Subject',
            labels={'Average Score': 'Average Score (%)', 'Subject': 'Subject'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.markdown("### 📋 Recent Activity")
    recent_activity = progress_data.get('recent_activity', [])
    
    if recent_activity:
        for activity in recent_activity[-10:]:  # Show last 10 activities
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"**{activity['type']}:** {activity['description']}")
                
                with col2:
                    st.markdown(f"📅 {activity['date']}")
                
                with col3:
                    if 'score' in activity:
                        st.markdown(f"📊 {activity['score']}%")
    else:
        st.info("No recent activity to display.")

def knowledge_base_interface():
    """Knowledge Base and Information Retrieval Interface"""
    st.header("🔍 Knowledge Base Search")
    st.markdown("Search and explore educational resources and knowledge.")
    
    from utils.information_retrieval import InformationRetrieval
    ir_system = InformationRetrieval()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search Knowledge Base",
            placeholder="Enter your search query..."
        )
    
    with col2:
        search_type = st.selectbox(
            "🎯 Search Type",
            ["General", "Definitions", "Examples", "Tutorials"]
        )
    
    if st.button("🔍 Search", type="primary"):
        if search_query:
            with st.spinner("🔍 Searching knowledge base..."):
                try:
                    clean_query = security.sanitize_input(search_query)
                    results = ir_system.search(clean_query, search_type)
                    
                    if results:
                        st.success(f"✅ Found {len(results)} results")
                        
                        for i, result in enumerate(results, 1):
                            with st.expander(f"📖 Result {i}: {result['title']}", expanded=i==1):
                                st.markdown(f"**Source:** {result.get('source', 'AI Generated')}")
                                st.markdown(f"**Relevance:** {result.get('relevance_score', 0):.2f}")
                                st.markdown("---")
                                st.markdown(result['content'])
                                
                                if result.get('related_topics'):
                                    st.markdown("**Related Topics:**")
                                    for topic in result['related_topics']:
                                        st.markdown(f"- {topic}")
                    else:
                        st.info("🔍 No results found. Try different keywords.")
                        
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a search query.")
    
    # Popular topics
    st.markdown("### 🔥 Popular Topics")
    popular_topics = [
        "Python Programming", "Machine Learning", "Calculus", "Data Structures",
        "World War II", "Shakespeare", "Chemistry Basics", "Linear Algebra"
    ]
    
    cols = st.columns(4)
    for i, topic in enumerate(popular_topics):
        with cols[i % 4]:
            if st.button(f"📚 {topic}", key=f"topic_{i}"):
                st.session_state.search_query = topic
                st.rerun()

# Main application flow
def main():
    authenticate_user()
    
    if st.session_state.current_user:
        main_interface()
    else:
        st.title("🎓 Welcome to AI Tutoring System")
        st.markdown("""
        ### 🚀 Multi-Agent Educational Platform
        
        Our AI-powered tutoring system features three specialized agents:
        
        - **📚 Content Generator**: Creates personalized educational content
        - **❓ Question Setter**: Generates assessments and practice questions  
        - **✅ Feedback Evaluator**: Provides detailed performance analysis
        
        **Features:**
        - 🤖 Advanced AI-powered learning
        - 📊 Progress tracking and analytics
        - 🔍 Comprehensive knowledge base
        - 🎯 Personalized feedback
        - 🌓 Dark mode support
        
        Please log in to start your learning journey!
        """)

if __name__ == "__main__":
    main()
