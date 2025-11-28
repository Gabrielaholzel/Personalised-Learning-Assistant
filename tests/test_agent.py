"""Integration tests for the Personalised Learning Assistant."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from learning_assistant import LearningOrchestrator
from learning_assistant.config import config


def test_create_learning_package():
    """Test creating a complete learning package."""
    print("=" * 60)
    print("TEST: Create Learning Package")
    print("=" * 60)
    print()
    
    try:
        # Validate config
        config.validate()
        
        # Create orchestrator
        orchestrator = LearningOrchestrator()
        
        # Create learning package
        topic = "Python Programming"
        goal = "Learn basic Python syntax and concepts"
        
        package = orchestrator.create_learning_package(
            topic=topic,
            goal=goal,
            user_id="test_user",
            num_questions=3
        )
        
        # Verify package structure
        assert "topic" in package
        assert "goal" in package
        assert "difficulty" in package
        assert "research" in package
        assert "learning_plan" in package
        assert "quiz" in package
        
        assert package["topic"] == topic
        assert package["goal"] == goal
        assert len(package["quiz"]) > 0
        
        print("✅ TEST PASSED: Learning package created successfully")
        print()
        print(f"Topic: {package['topic']}")
        print(f"Difficulty: {package['difficulty']}")
        print(f"Quiz Questions: {len(package['quiz'])}")
        print()
        
        return package
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        raise


def test_evaluate_quiz(package):
    """Test quiz evaluation and progress tracking."""
    print("=" * 60)
    print("TEST: Evaluate Quiz")
    print("=" * 60)
    print()
    
    try:
        orchestrator = LearningOrchestrator()
        
        # Simulate user answers (all correct for testing)
        user_answers = {
            i: q["correct"] for i, q in enumerate(package["quiz"])
        }
        
        # Evaluate quiz
        results = orchestrator.evaluate_quiz(
            quiz_questions=package["quiz"],
            user_answers=user_answers,
            topic=package["topic"],
            user_id="test_user"
        )
        
        # Verify results structure
        assert "score" in results
        assert "total" in results
        assert "percentage" in results
        assert "results" in results
        assert "new_difficulty" in results
        
        assert results["score"] == results["total"]  # All correct
        assert results["percentage"] == 100.0
        
        print("✅ TEST PASSED: Quiz evaluated successfully")
        print()
        print(f"Score: {results['score']}/{results['total']} ({results['percentage']:.1f}%)")
        print(f"New Difficulty: {results['new_difficulty']}")
        print(f"Recommendation: {results['recommendation']}")
        print()
        
        return results
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        raise


def test_user_dashboard():
    """Test user dashboard retrieval."""
    print("=" * 60)
    print("TEST: User Dashboard")
    print("=" * 60)
    print()
    
    try:
        orchestrator = LearningOrchestrator()
        
        # Get dashboard
        dashboard = orchestrator.get_user_dashboard(user_id="test_user")
        
        # Verify dashboard structure
        assert "user_id" in dashboard
        assert "current_difficulty" in dashboard
        assert "topics_studied" in dashboard
        assert "total_quizzes" in dashboard
        assert "average_score" in dashboard
        
        print("✅ TEST PASSED: Dashboard retrieved successfully")
        print()
        print(f"User ID: {dashboard['user_id']}")
        print(f"Current Difficulty: {dashboard['current_difficulty']}")
        print(f"Topics Studied: {len(dashboard['topics_studied'])}")
        print(f"Total Quizzes: {dashboard['total_quizzes']}")
        print(f"Average Score: {dashboard['average_score']:.1f}%")
        print(f"Recommendation: {dashboard['recommendation']}")
        print()
        
        return dashboard
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        raise


def run_all_tests():
    """Run all integration tests."""
    print()
    print("🧪 RUNNING INTEGRATION TESTS")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Create learning package
        package = test_create_learning_package()
        
        # Test 2: Evaluate quiz
        results = test_evaluate_quiz(package)
        
        # Test 3: Get user dashboard
        dashboard = test_user_dashboard()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ TESTS FAILED")
        print("=" * 60)
        print()
        raise


if __name__ == "__main__":
    run_all_tests()
