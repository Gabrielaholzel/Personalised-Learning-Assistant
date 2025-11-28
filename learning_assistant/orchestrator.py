"""Learning Orchestrator - Coordinates all agents to create complete learning experiences."""

from typing import Dict, List

from learning_assistant.agents import (
    ResearchAgent,
    ContentAgent,
    QuizAgent,
    PersonalisationEngine
)
from learning_assistant.config import config


class LearningOrchestrator:
    """
    Main orchestrator that coordinates all agents to create
    complete personalised learning experiences.
    
    This orchestrator follows a sequential workflow:
    1. Load user progress and get current difficulty level
    2. Research Agent fetches and summarises topic information
    3. Content Agent generates personalised learning plan
    4. Quiz Agent creates adaptive assessment
    5. Evaluate user answers and provide feedback
    6. Personalisation Engine updates progress and adapts difficulty
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialise the Learning Orchestrator with all agents.
        
        Args:
            api_key: Google Gemini API key (optional, uses config if not provided)
        """
        api_key = api_key or config.GEMINI_API_KEY
        
        # Validate configuration
        config.validate()
        
        # Initialise all agents
        self.research_agent = ResearchAgent(api_key)
        self.content_agent = ContentAgent(api_key)
        self.quiz_agent = QuizAgent(api_key)
        self.personalisation_engine = PersonalisationEngine()
    
    def create_learning_package(self, topic: str, goal: str, 
                               user_id: str = "default",
                               num_questions: int = None) -> Dict:
        """
        Orchestrate the creation of a complete learning package.
        
        This method coordinates all agents to:
        1. Fetch and summarise topic information
        2. Generate a personalised learning plan
        3. Create an adaptive quiz
        
        Args:
            topic: The topic to learn about
            goal: User's learning objective
            user_id: Unique identifier for the user
            num_questions: Number of quiz questions (optional, uses config default)
            
        Returns:
            Dictionary containing:
                - topic: The topic
                - goal: The learning goal
                - difficulty: Current difficulty level
                - research: Research data (raw and structured summary)
                - learning_plan: Personalised learning plan
                - quiz: List of quiz questions
        """
        # Get user's current difficulty level
        progress = self.personalisation_engine.load_progress(user_id)
        difficulty = progress.get("current_difficulty", config.DEFAULT_DIFFICULTY)
        
        print(f"📚 Creating learning package for '{topic}'...")
        print(f"🎯 Goal: {goal}")
        print(f"📊 Difficulty Level: {difficulty.upper()}")
        print()
        
        # Step 1: Research
        print("🔍 Step 1: Researching topic...")
        research_data = self.research_agent.fetch_topic_info(topic)
        print("✓ Research complete")
        print()
        
        # Step 2: Generate Learning Plan
        print(f"📝 Step 2: Generating learning plan (Difficulty: {difficulty})...")
        learning_plan = self.content_agent.generate_learning_plan(topic, goal, difficulty)
        print("✓ Learning plan generated")
        print()
        
        # Step 3: Create Quiz
        num_q = num_questions or config.DEFAULT_NUM_QUESTIONS
        print(f"❓ Step 3: Creating {num_q}-question quiz...")
        quiz = self.quiz_agent.generate_quiz(topic, difficulty, num_q)
        print(f"✓ Quiz created ({len(quiz)} questions)")
        print()
        
        print("✅ Learning package complete!")
        print()
        
        return {
            "topic": topic,
            "goal": goal,
            "difficulty": difficulty,
            "research": research_data,
            "learning_plan": learning_plan,
            "quiz": quiz
        }
    
    def evaluate_quiz(self, quiz_questions: List[Dict], user_answers: Dict[int, str], 
                     topic: str, user_id: str = "default") -> Dict:
        """
        Evaluate quiz answers and update user progress.
        
        This method:
        1. Evaluates each answer using the Quiz Agent
        2. Calculates overall score
        3. Updates user progress via Personalisation Engine
        4. Returns detailed results with new difficulty level
        
        Args:
            quiz_questions: List of question dictionaries
            user_answers: Dictionary mapping question index to user's answer
            topic: Topic of the quiz
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary containing:
                - score: Number of correct answers
                - total: Total number of questions
                - percentage: Score as a percentage
                - results: Detailed results for each question
                - new_difficulty: Updated difficulty level
                - recommendation: Personalised recommendation
        """
        print("📊 Evaluating quiz...")
        
        # Evaluate using Quiz Agent
        evaluation = self.quiz_agent.evaluate_quiz(quiz_questions, user_answers)
        
        # Update progress using Personalisation Engine
        updated_progress = self.personalisation_engine.update_quiz_score(
            user_id, 
            topic, 
            evaluation["score"], 
            evaluation["total"]
        )
        
        # Get recommendations
        recommendations = self.personalisation_engine.get_recommendations(user_id)
        
        print(f"✓ Quiz evaluated: {evaluation['score']}/{evaluation['total']} ({evaluation['percentage']:.1f}%)")
        print(f"📈 New difficulty level: {updated_progress['current_difficulty'].upper()}")
        print()
        
        return {
            **evaluation,
            "new_difficulty": updated_progress["current_difficulty"],
            "recommendation": recommendations["suggestion"]
        }
    
    def get_user_dashboard(self, user_id: str = "default") -> Dict:
        """
        Get comprehensive user progress dashboard.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary containing progress summary and recommendations
        """
        return self.personalisation_engine.get_progress_summary(user_id)
    
    def generate_lesson(self, topic: str, module_name: str, 
                       user_id: str = "default") -> str:
        """
        Generate a detailed lesson for a specific module.
        
        Args:
            topic: The overall topic
            module_name: Specific module to create lesson for
            user_id: Unique identifier for the user
            
        Returns:
            Detailed lesson content as a string
        """
        # Get user's current difficulty level
        progress = self.personalisation_engine.load_progress(user_id)
        difficulty = progress.get("current_difficulty", config.DEFAULT_DIFFICULTY)
        
        print(f"📖 Generating lesson: {module_name}")
        print(f"📊 Difficulty: {difficulty.upper()}")
        print()
        
        lesson = self.content_agent.generate_lesson(topic, module_name, difficulty)
        
        print("✓ Lesson generated")
        print()
        
        return lesson
