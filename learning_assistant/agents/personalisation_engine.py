"""Personalisation Engine - Tracks progress and adapts difficulty."""

import os
import json
from typing import Dict, List
from datetime import datetime

from learning_assistant.config import config
from learning_assistant.tools import (
    load_user_progress,
    save_user_progress,
    calculate_difficulty,
    get_recommendations
)


class PersonalisationEngine:
    """
    Personalisation Engine that tracks user progress across sessions,
    calculates adaptive difficulty, and provides personalised recommendations.
    """
    
    def __init__(self, storage_path: str = None):
        """
        Initialise the Personalisation Engine.
        
        Args:
            storage_path: Path to progress storage file (optional, uses config if not provided)
        """
        self.storage_path = storage_path or config.PROGRESS_FILE_PATH
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory and file exist."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)
    
    def load_progress(self, user_id: str = "default") -> Dict:
        """
        Load user progress from storage.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary containing user progress data:
                - topics_studied: List of topics the user has studied
                - quiz_scores: List of quiz score records
                - current_difficulty: Current difficulty level
                - total_time: Total time spent (placeholder for future use)
        """
        return load_user_progress(user_id, self.storage_path)
    
    def save_progress(self, user_id: str, progress_data: Dict):
        """
        Save user progress to storage.
        
        Args:
            user_id: Unique identifier for the user
            progress_data: Dictionary containing progress data to save
        """
        save_user_progress(user_id, progress_data, self.storage_path)
    
    def update_quiz_score(self, user_id: str, topic: str, score: int, total: int) -> Dict:
        """
        Update user's quiz score and recalculate difficulty.
        
        This method:
        1. Adds the new quiz score to the user's history
        2. Updates the list of topics studied
        3. Recalculates the appropriate difficulty level
        4. Saves the updated progress
        
        Args:
            user_id: Unique identifier for the user
            topic: Topic of the quiz
            score: Number of correct answers
            total: Total number of questions
            
        Returns:
            Updated progress data dictionary
        """
        progress = self.load_progress(user_id)
        
        # Add new quiz score
        progress["quiz_scores"].append({
            "topic": topic,
            "score": score,
            "total": total,
            "percentage": (score / total) * 100,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update topics studied
        if topic not in progress["topics_studied"]:
            progress["topics_studied"].append(topic)
        
        # Adapt difficulty based on performance
        progress["current_difficulty"] = self._calculate_difficulty(progress["quiz_scores"])
        
        # Save updated progress
        self.save_progress(user_id, progress)
        
        return progress
    
    def _calculate_difficulty(self, quiz_scores: List[Dict]) -> str:
        """
        Calculate appropriate difficulty level based on recent performance.
        
        Uses the last N quiz scores (configured in config.RECENT_SCORES_COUNT)
        to determine if the user should move up or down in difficulty.
        
        Args:
            quiz_scores: List of quiz score dictionaries
            
        Returns:
            Difficulty level: "beginner", "intermediate", or "advanced"
        """
        return calculate_difficulty(quiz_scores, config.RECENT_SCORES_COUNT)
    
    def get_recommendations(self, user_id: str) -> Dict:
        """
        Get personalised recommendations for the user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary containing:
                - difficulty: Current difficulty level
                - topics_completed: Number of topics studied
                - average_score: Average quiz score percentage
                - suggestion: Personalised suggestion text
        """
        return get_recommendations(user_id, self.storage_path)
    
    def get_progress_summary(self, user_id: str) -> Dict:
        """
        Get a comprehensive summary of user progress.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary containing progress summary and recommendations
        """
        progress = self.load_progress(user_id)
        recommendations = self.get_recommendations(user_id)
        
        # Calculate additional statistics
        total_quizzes = len(progress["quiz_scores"])
        recent_scores = progress["quiz_scores"][-5:] if progress["quiz_scores"] else []
        
        return {
            "user_id": user_id,
            "current_difficulty": progress["current_difficulty"],
            "topics_studied": progress["topics_studied"],
            "total_quizzes": total_quizzes,
            "recent_scores": recent_scores,
            "average_score": recommendations["average_score"],
            "recommendation": recommendations["suggestion"]
        }
    
    def reset_progress(self, user_id: str):
        """
        Reset user progress (useful for testing or starting fresh).
        
        Args:
            user_id: Unique identifier for the user
        """
        fresh_progress = {
            "topics_studied": [],
            "quiz_scores": [],
            "current_difficulty": "beginner",
            "total_time": 0
        }
        self.save_progress(user_id, fresh_progress)
