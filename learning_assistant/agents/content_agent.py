"""Content Agent - Generates personalised learning plans and lessons."""

import google.generativeai as genai

from learning_assistant.config import config


class ContentAgent:
    """
    Content Generator Agent that creates structured learning plans
    and lessons adapted to user's difficulty level.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialise the Content Agent.
        
        Args:
            api_key: Google Gemini API key (optional, uses config if not provided)
        """
        api_key = api_key or config.GEMINI_API_KEY
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
    
    def generate_learning_plan(self, topic: str, goal: str, 
                              difficulty: str = "beginner") -> str:
        """
        Generate a structured learning plan adapted to difficulty level.
        
        Args:
            topic: The subject to create a plan for
            goal: User's learning objective
            difficulty: Current difficulty level (beginner/intermediate/advanced)
            
        Returns:
            Structured learning plan as a string
        """
        # Adapt prompt based on difficulty
        difficulty_context = {
            "beginner": "Focus on fundamentals and basic concepts. Use simple language and provide plenty of examples.",
            "intermediate": "Build on foundational knowledge. Include more technical details and practical applications.",
            "advanced": "Assume strong foundational knowledge. Focus on advanced concepts, edge cases, and expert-level insights."
        }
        
        context = difficulty_context.get(difficulty, difficulty_context["beginner"])
        
        prompt = f"""Create a detailed learning plan for: {topic}

Learning Goal: {goal}
Difficulty Level: {difficulty}

{context}

Structure the plan as:
1. Learning Objectives (3-5 specific, measurable goals)
2. Prerequisites (if any - what should learners know before starting)
3. Learning Path (5-7 modules with brief descriptions)
   - Each module should build on the previous one
   - Include estimated time for each module
4. Estimated Total Time
5. Resources & Next Steps

Make it practical, engaging, and tailored to the {difficulty} level."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_lesson(self, topic: str, module_name: str, 
                       difficulty: str = "beginner") -> str:
        """
        Generate detailed lesson content for a specific module.
        
        Args:
            topic: The overall topic
            module_name: Specific module to create lesson for
            difficulty: Current difficulty level
            
        Returns:
            Detailed lesson content as a string
        """
        difficulty_context = {
            "beginner": "Use simple language, provide step-by-step explanations, and include basic examples.",
            "intermediate": "Include technical details, practical applications, and real-world scenarios.",
            "advanced": "Focus on complex concepts, advanced techniques, and expert-level insights."
        }
        
        context = difficulty_context.get(difficulty, difficulty_context["beginner"])
        
        prompt = f"""Create a comprehensive lesson on: {module_name} (part of {topic})

Difficulty: {difficulty}

{context}

Include:
1. Introduction & Context (why this module matters)
2. Core Concepts (with clear explanations)
   - Break down complex ideas into digestible parts
   - Use analogies where helpful
3. Examples (2-3 practical examples)
   - Show real-world applications
   - Include step-by-step walkthroughs
4. Key Takeaways (3-5 main points to remember)
5. Practice Suggestions (how to apply this knowledge)

Make it engaging, educational, and appropriate for {difficulty} level learners."""
        
        response = self.model.generate_content(prompt)
        return response.text
