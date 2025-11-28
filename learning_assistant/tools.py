"""Custom tools for the Personalised Learning Assistant."""

import json
import os
from typing import Dict, List
from datetime import datetime


def ensure_data_directory():
    """Ensure the data directory exists."""
    os.makedirs("data", exist_ok=True)


def load_user_progress(user_id: str = "default", storage_path: str = "data/progress.json") -> Dict:
    """
    Load user progress from storage.
    
    Args:
        user_id: Unique identifier for the user
        storage_path: Path to the progress storage file
        
    Returns:
        Dictionary containing user progress data
    """
    ensure_data_directory()
    
    if not os.path.exists(storage_path):
        with open(storage_path, 'w') as f:
            json.dump({}, f)
    
    with open(storage_path, 'r') as f:
        data = json.load(f)
    
    return data.get(user_id, {
        "topics_studied": [],
        "quiz_scores": [],
        "current_difficulty": "beginner",
        "total_time": 0
    })


def save_user_progress(user_id: str, progress_data: Dict, storage_path: str = "data/progress.json"):
    """
    Save user progress to storage.
    
    Args:
        user_id: Unique identifier for the user
        progress_data: Dictionary containing progress data to save
        storage_path: Path to the progress storage file
    """
    ensure_data_directory()
    
    if not os.path.exists(storage_path):
        data = {}
    else:
        with open(storage_path, 'r') as f:
            data = json.load(f)
    
    data[user_id] = progress_data
    
    with open(storage_path, 'w') as f:
        json.dump(data, f, indent=2)


def calculate_difficulty(quiz_scores: List[Dict], recent_count: int = 3) -> str:
    """
    Calculate appropriate difficulty level based on recent performance.
    
    Args:
        quiz_scores: List of quiz score dictionaries
        recent_count: Number of recent scores to consider
        
    Returns:
        Difficulty level: "beginner", "intermediate", or "advanced"
    """
    if not quiz_scores:
        return "beginner"
    
    recent_scores = quiz_scores[-recent_count:]
    avg_percentage = sum(q["percentage"] for q in recent_scores) / len(recent_scores)
    
    if avg_percentage >= 85:
        return "advanced"
    elif avg_percentage >= 70:
        return "intermediate"
    else:
        return "beginner"


def update_quiz_score(user_id: str, topic: str, score: int, total: int, 
                      storage_path: str = "data/progress.json") -> Dict:
    """
    Update user's quiz score and recalculate difficulty.
    
    Args:
        user_id: Unique identifier for the user
        topic: Topic of the quiz
        score: Number of correct answers
        total: Total number of questions
        storage_path: Path to the progress storage file
        
    Returns:
        Updated progress data
    """
    progress = load_user_progress(user_id, storage_path)
    
    progress["quiz_scores"].append({
        "topic": topic,
        "score": score,
        "total": total,
        "percentage": (score / total) * 100,
        "timestamp": datetime.now().isoformat()
    })
    
    if topic not in progress["topics_studied"]:
        progress["topics_studied"].append(topic)
    
    # Adapt difficulty based on performance
    progress["current_difficulty"] = calculate_difficulty(progress["quiz_scores"])
    
    save_user_progress(user_id, progress, storage_path)
    return progress


def get_recommendations(user_id: str, storage_path: str = "data/progress.json") -> Dict:
    """
    Get personalised recommendations for the user.
    
    Args:
        user_id: Unique identifier for the user
        storage_path: Path to the progress storage file
        
    Returns:
        Dictionary containing recommendations
    """
    progress = load_user_progress(user_id, storage_path)
    
    recommendations = {
        "difficulty": progress["current_difficulty"],
        "topics_completed": len(progress["topics_studied"]),
        "average_score": 0,
        "suggestion": ""
    }
    
    if progress["quiz_scores"]:
        avg_score = sum(q["percentage"] for q in progress["quiz_scores"]) / len(progress["quiz_scores"])
        recommendations["average_score"] = round(avg_score, 1)
        
        if avg_score >= 80:
            recommendations["suggestion"] = "Great progress! Try more advanced topics."
        elif avg_score >= 60:
            recommendations["suggestion"] = "Good work! Keep practising to improve."
        else:
            recommendations["suggestion"] = "Review fundamentals and try easier topics."
    else:
        recommendations["suggestion"] = "Start your learning journey!"
    
    return recommendations


def export_learning_package(package: Dict, filename: str = "learning_package.json"):
    """
    Export a learning package to a JSON file.
    
    Args:
        package: Learning package dictionary
        filename: Output filename
    """
    ensure_data_directory()
    filepath = os.path.join("data", filename)
    
    with open(filepath, 'w') as f:
        json.dump(package, f, indent=2)
    
    return filepath
