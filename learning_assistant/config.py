"""Configuration for the Personalised Learning Assistant agents."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for agent settings."""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Model Configuration
    MODEL_NAME = "gemini-2.5-flash"
    
    # Quiz Configuration
    DEFAULT_NUM_QUESTIONS = 5
    DEFAULT_DIFFICULTY = "beginner"
    
    # Difficulty Thresholds
    ADVANCED_THRESHOLD = 85  # >= 85% average score
    INTERMEDIATE_THRESHOLD = 70  # >= 70% average score
    
    # Progress Tracking
    PROGRESS_FILE_PATH = "data/progress.json"
    RECENT_SCORES_COUNT = 3  # Number of recent scores to consider for difficulty
    
    # Wikipedia Configuration
    WIKIPEDIA_SENTENCES = 10
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your .env file. "
                "Get your API key from: https://makersuite.google.com/app/apikey"
            )
        return True

config = Config()
