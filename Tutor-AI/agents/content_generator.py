import json
import os
import google.generativeai as genai
from google.generativeai import types
from utils.nlp_processor import NLPProcessor
from utils.information_retrieval import InformationRetrieval

class ContentGeneratorAgent:
    """
    Content Generator Agent for creating educational content using LLMs
    Integrates with NLP processing and information retrieval systems
    """
    
    def __init__(self):
        # Using Google Gemini 2.5 Flash for free AI content generation
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.nlp_processor = NLPProcessor()
        self.ir_system = InformationRetrieval()
        self.agent_id = "content_generator"
    
    def generate_content(self, topic, difficulty="Intermediate", subject="General", content_type="Lesson", learning_objectives=None):
        """
        Generate educational content with improved retrieval and NLP processing
        
        Args:
            topic (str): The topic to generate content for
            difficulty (str): Difficulty level (Beginner, Intermediate, Advanced)
            subject (str): Subject area
            content_type (str): Type of content to generate
            learning_objectives (list): Specific learning goals to focus on
            
        Returns:
            dict: Generated educational content with metadata
        """
        try:
            # Phase 1: Retrieve reliable sources and context
            sources = self._retrieve_reliable_sources(topic, subject)
            context = self._gather_enhanced_context(topic, subject, sources)
            
            # Phase 2: Generate student-friendly content
            content = self._generate_student_friendly_content(
                topic, difficulty, subject, content_type, context, learning_objectives
            )
            
            # Phase 3: NLP processing for key concepts and structure
            processed_content = self._advanced_nlp_processing(content, topic)
            
            # Phase 4: Create study materials (notes, flashcards, diagrams)
            study_materials = self._create_study_materials(processed_content, topic)
            
            return {
                'content': processed_content,
                'study_materials': study_materials,
                'key_concepts': study_materials.get('key_concepts', []),
                'learning_objectives': study_materials.get('learning_objectives', []),
                'difficulty_level': difficulty,
                'sources': sources
            }
            
        except Exception as e:
            raise Exception(f"Content generation failed: {str(e)}")
    
    def _retrieve_reliable_sources(self, topic, subject):
        """Retrieve reliable educational sources"""
        try:
            # Search multiple source types
            academic_sources = self.ir_system.search(f"{topic} {subject} academic textbook", "Academic")
            web_sources = self.ir_system.search(f"{topic} {subject} educational", "Educational")
            
            return {
                'academic': academic_sources[:3],
                'educational': web_sources[:3],
                'quality_score': self._assess_source_quality(academic_sources + web_sources)
            }
        except Exception:
            return {'academic': [], 'educational': [], 'quality_score': 0.5}
    
    def _gather_enhanced_context(self, topic, subject, sources):
        """Enhanced context gathering with source reliability"""
        try:
            context_parts = []
            
            # Prioritize academic sources
            for source in sources.get('academic', []):
                context_parts.append(f"Academic Source: {source.get('title', 'Unknown')}\n{source.get('content', '')}")
            
            # Add educational sources
            for source in sources.get('educational', []):
                context_parts.append(f"Educational Source: {source.get('title', 'Unknown')}\n{source.get('content', '')}")
            
            return "\n\n".join(context_parts)
        except Exception:
            return ""
    
    def _assess_source_quality(self, sources):
        """Assess quality of retrieved sources"""
        if not sources:
            return 0.0
        
        quality_indicators = ['academic', 'peer-reviewed', 'textbook', 'educational', 'university']
        total_score = 0
        
        for source in sources:
            score = 0
            content = (source.get('title', '') + ' ' + source.get('content', '')).lower()
            for indicator in quality_indicators:
                if indicator in content:
                    score += 1
            total_score += score / len(quality_indicators)
        
        return min(total_score / len(sources), 1.0)
    
    def _gather_context(self, topic, subject):
        """Gather relevant context using information retrieval"""
        try:
            search_results = self.ir_system.search(f"{topic} {subject}", "General")
            
            if search_results:
                # Combine top 3 results for context
                context_parts = []
                for result in search_results[:3]:
                    context_parts.append(result['content'][:500])  # Limit context size
                
                return " ".join(context_parts)
            
            return ""
            
        except Exception:
            return ""  # Fallback to no additional context
    
    def _generate_with_llm(self, topic, difficulty, subject, content_type, context):
        """Generate content using OpenAI GPT with natural flow"""
        
        system_prompt = f"""You are an expert educator specializing in {subject}. 
        Create engaging, natural educational content that:
        - Feels conversational and approachable for {difficulty} level learners
        - Uses varied sentence structures and natural flow
        - Includes relevant examples and real-world connections
        - Avoids rigid templates - let the content flow naturally
        - Maintains educational value while being engaging
        
        Content Type: {content_type}
        Subject Area: {subject}
        Difficulty Level: {difficulty}
        """
        
        user_prompt = f"""Create engaging educational content about: {topic}
        
        {f"Additional Context: {context}" if context else ""}
        
        Write in a natural, conversational style. Don't force a rigid structure - let the content flow organically. 
        Include an engaging introduction, clear explanations with varied examples, practical applications, 
        and a meaningful conclusion. Vary your approach and make it feel like a knowledgeable teacher 
        having a conversation with students.
        """
        
        response = self.model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        return response.text or "Content generation failed"
    
    def _generate_student_friendly_content(self, topic, difficulty, subject, content_type, context, learning_objectives):
        """Generate student-friendly content with natural, varied structure"""
        objectives_text = ""
        if learning_objectives:
            objectives_text = f"Focus on these learning objectives: {', '.join(learning_objectives)}"
        
        # Create varied content styles based on content type
        content_styles = {
            "Study Notes": "Create natural, flowing study notes that feel like a knowledgeable friend explaining the topic. Use conversational language, varied sentence structures, and natural transitions.",
            "Tutorial": "Write a hands-on tutorial with step-by-step guidance. Include practical examples and encourage experimentation.",
            "Explanation": "Provide a clear, logical explanation that builds understanding progressively. Use analogies and real-world connections.",
            "Summary": "Create a concise but comprehensive overview that captures the essence of the topic.",
            "Comprehensive Guide": "Write an in-depth exploration that covers all aspects of the topic with natural flow and varied presentation."
        }
        
        style_guide = content_styles.get(content_type, content_styles["Study Notes"])
        
        system_prompt = f"""You are an expert educator and content creator specializing in {subject}. 
        Create engaging, natural educational content that:
        - Feels conversational and approachable for {difficulty} level learners
        - Uses varied sentence structures and natural flow
        - Includes relevant examples, analogies, and real-world connections
        - Avoids rigid templates - let the content flow naturally
        - Maintains educational value while being engaging
        
        Content Type: {content_type}
        Subject Area: {subject}
        Difficulty Level: {difficulty}
        Style: {style_guide}
        {objectives_text}
        """
        
        user_prompt = f"""Create engaging educational content about: {topic}
        
        {f"Reference Material: {context}" if context else ""}
        
        Write in a natural, conversational style. Don't force a rigid structure - let the content flow organically. 
        Include:
        - An engaging introduction that captures interest
        - Clear explanations with varied examples
        - Practical applications and real-world connections
        - Helpful tips and insights
        - A meaningful conclusion
        
        Vary your approach - use different paragraph styles, mix short and long sentences, 
        include questions, analogies, and natural transitions. Make it feel like a knowledgeable 
        teacher having a conversation with students.
        """
        
        response = self.model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        return response.text or "Content generation failed"
    
    def _advanced_nlp_processing(self, content, topic):
        """Advanced NLP processing for key concepts and structure"""
        try:
            # Extract key entities and concepts using NLP
            entities = self.nlp_processor.extract_entities(content)
            key_terms = self.nlp_processor.extract_key_terms(content)
            
            # Generate improved summary
            summary = self.nlp_processor.summarize_text(content)
            
            # Create structured content with NLP insights
            enhanced_content = f"""# {topic}
            
{content}

---

## 📋 Executive Summary
{summary}

## 🔑 Key Terms Identified
{', '.join([term for term in key_terms[:15]])}

## 🎯 Important Concepts  
{', '.join([ent['text'] for ent in entities[:10]])}

## 📚 Learning Objectives
- Understand the fundamental concepts of {topic}
- Apply knowledge in practical scenarios
- Identify key relationships and connections
- Analyze real-world applications

"""
            
            return enhanced_content
            
        except Exception:
            # Fallback to original content if NLP processing fails
            return content
    
    def _create_study_materials(self, content, topic):
        """Create comprehensive study materials including flashcards and diagrams"""
        try:
            # Extract key concepts for flashcards
            entities = self.nlp_processor.extract_entities(content)
            key_terms = self.nlp_processor.extract_key_terms(content)
            
            # Create flashcard concepts
            flashcard_concepts = []
            for entity in entities[:10]:
                flashcard_concepts.append({
                    'term': entity['text'],
                    'definition': f"Key concept in {topic}",
                    'category': entity.get('label', 'CONCEPT')
                })
            
            # Generate learning objectives
            objectives = [
                f"Define and explain {topic}",
                f"Identify key components of {topic}",
                f"Apply {topic} concepts to real-world scenarios",
                f"Analyze relationships within {topic}"
            ]
            
            return {
                'flashcards': flashcard_concepts,
                'key_concepts': [ent['text'] for ent in entities[:15]],
                'learning_objectives': objectives,
                'study_notes': self._create_bullet_notes(content),
                'diagram_suggestions': self._suggest_diagrams(topic, entities)
            }
            
        except Exception:
            return {
                'flashcards': [],
                'key_concepts': [],
                'learning_objectives': [],
                'study_notes': '',
                'diagram_suggestions': []
            }
    
    def _create_bullet_notes(self, content):
        """Create bullet-point study notes from content"""
        lines = content.split('\n')
        bullet_notes = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 20 and not line.startswith('#'):
                if '.' in line and len(line) < 200:  # Good for bullet points
                    bullet_notes.append(f"• {line}")
        
        return '\n'.join(bullet_notes[:15])  # Limit to 15 key points
    
    def _suggest_diagrams(self, topic, entities):
        """Suggest diagram types based on topic and entities"""
        suggestions = []
        
        # Common diagram types for educational content
        if any(word in topic.lower() for word in ['process', 'cycle', 'steps']):
            suggestions.append('Process Flow Diagram')
        
        if any(word in topic.lower() for word in ['structure', 'anatomy', 'parts']):
            suggestions.append('Labeled Diagram')
        
        if any(word in topic.lower() for word in ['compare', 'vs', 'difference']):
            suggestions.append('Comparison Chart')
        
        if len(entities) > 5:
            suggestions.append('Mind Map')
            suggestions.append('Concept Map')
        
        suggestions.append('Summary Infographic')
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _enhance_content(self, content, topic):
        """Enhance content using NLP processing"""
        try:
            # Extract key entities and concepts
            entities = self.nlp_processor.extract_entities(content)
            
            # Generate summary
            summary = self.nlp_processor.summarize_text(content)
            
            # Add NLP enhancements to content
            enhanced_content = f"""# {topic}

{content}

---

## 📋 Key Summary
{summary}

## 🔑 Key Concepts Identified
{', '.join([ent['text'] for ent in entities[:10]])}  

"""
            
            return enhanced_content
            
        except Exception:
            # Fallback to original content if NLP processing fails
            return content
    
    def generate_structured_content(self, topic, structure_type="standard"):
        """Generate content with specific structure"""
        
        structures = {
            "standard": ["Introduction", "Main Content", "Examples", "Conclusion"],
            "tutorial": ["Prerequisites", "Step-by-Step Guide", "Practice Exercises", "Troubleshooting"],
            "explanation": ["What is it?", "How does it work?", "Why is it important?", "Real-world applications"],
            "comparison": ["Overview", "Similarities", "Differences", "When to use each", "Conclusion"]
        }
        
        structure = structures.get(structure_type, structures["standard"])
        
        structured_prompt = f"""Create educational content about {topic} using this structure:

{chr(10).join([f"{i+1}. {section}" for i, section in enumerate(structure)])}

Make each section comprehensive and educational."""
        
        response = self.model.generate_content(f"You are an expert educational content creator.\n\n{structured_prompt}")
        
        return response.text or "Structured content generation failed"
    
    def adapt_content_difficulty(self, content, target_difficulty):
        """Adapt existing content to different difficulty level"""
        
        adaptation_prompt = f"""Adapt the following educational content to {target_difficulty} level:

{content}

Adjust:
- Vocabulary complexity
- Concept depth
- Examples used
- Explanations detail

Make it appropriate for {target_difficulty} learners while maintaining accuracy."""
        
        response = self.model.generate_content(f"You are an expert at adapting educational content for different skill levels.\n\n{adaptation_prompt}")
        
        return response.text or "Content adaptation failed"
