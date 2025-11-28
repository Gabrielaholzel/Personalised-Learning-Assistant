"""
Example usage of the Personalised Learning Assistant.

This script demonstrates how to use the LearningOrchestrator
to create learning packages and evaluate quizzes.
"""

from learning_assistant import LearningOrchestrator


def main():
    """Main example demonstrating the learning assistant."""
    
    print("=" * 70)
    print("PERSONALISED LEARNING ASSISTANT - EXAMPLE USAGE")
    print("=" * 70)
    print()
    
    # Initialize the orchestrator
    print("Initializing Learning Orchestrator...")
    orchestrator = LearningOrchestrator()
    print("✓ Orchestrator initialized")
    print()
    
    # Example 1: Create a learning package
    print("-" * 70)
    print("EXAMPLE 1: Creating a Learning Package")
    print("-" * 70)
    print()
    
    topic = "Python Programming"
    goal = "Learn basic Python syntax and concepts"
    user_id = "demo_user"
    
    package = orchestrator.create_learning_package(
        topic=topic,
        goal=goal,
        user_id=user_id,
        num_questions=3  # Fewer questions for demo
    )
    
    print("📦 Learning Package Created!")
    print(f"   Topic: {package['topic']}")
    print(f"   Difficulty: {package['difficulty']}")
    print(f"   Quiz Questions: {len(package['quiz'])}")
    print()
    
    # Display research summary
    print("-" * 70)
    print("RESEARCH SUMMARY")
    print("-" * 70)
    print(package['research']['structured_summary'][:500] + "...")
    print()
    
    # Display learning plan preview
    print("-" * 70)
    print("LEARNING PLAN (Preview)")
    print("-" * 70)
    print(package['learning_plan'][:500] + "...")
    print()
    
    # Display quiz questions
    print("-" * 70)
    print("QUIZ QUESTIONS")
    print("-" * 70)
    for i, question in enumerate(package['quiz'], 1):
        print(f"\nQ{i}: {question['question']}")
        for key, value in question['options'].items():
            print(f"   {key}) {value}")
    print()
    
    # Example 2: Simulate quiz taking and evaluation
    print("-" * 70)
    print("EXAMPLE 2: Taking and Evaluating Quiz")
    print("-" * 70)
    print()
    
    # Simulate user answers (for demo, we'll answer all correctly)
    print("Simulating user answers (all correct for demo)...")
    user_answers = {
        i: q['correct'] for i, q in enumerate(package['quiz'])
    }
    print(f"User answers: {user_answers}")
    print()
    
    # Evaluate the quiz
    results = orchestrator.evaluate_quiz(
        quiz_questions=package['quiz'],
        user_answers=user_answers,
        topic=topic,
        user_id=user_id
    )
    
    print("📊 Quiz Results:")
    print(f"   Score: {results['score']}/{results['total']}")
    print(f"   Percentage: {results['percentage']:.1f}%")
    print(f"   New Difficulty: {results['new_difficulty']}")
    print(f"   Recommendation: {results['recommendation']}")
    print()
    
    # Display detailed results
    print("-" * 70)
    print("DETAILED RESULTS")
    print("-" * 70)
    for result in results['results']:
        status = "✓ CORRECT" if result['is_correct'] else "✗ INCORRECT"
        print(f"\n{status} - Question {result['question_num']}")
        print(f"Q: {result['question']}")
        print(f"Your Answer: {result['user_answer']}")
        print(f"Correct Answer: {result['correct_answer']}")
        print(f"Explanation: {result['explanation'][:200]}...")
    print()
    
    # Example 3: View user dashboard
    print("-" * 70)
    print("EXAMPLE 3: User Dashboard")
    print("-" * 70)
    print()
    
    dashboard = orchestrator.get_user_dashboard(user_id=user_id)
    
    print("👤 User Dashboard:")
    print(f"   User ID: {dashboard['user_id']}")
    print(f"   Current Difficulty: {dashboard['current_difficulty']}")
    print(f"   Topics Studied: {len(dashboard['topics_studied'])}")
    if dashboard['topics_studied']:
        for topic in dashboard['topics_studied']:
            print(f"      - {topic}")
    print(f"   Total Quizzes: {dashboard['total_quizzes']}")
    print(f"   Average Score: {dashboard['average_score']:.1f}%")
    print(f"   Recommendation: {dashboard['recommendation']}")
    print()
    
    # Display recent scores
    if dashboard['recent_scores']:
        print("   Recent Quiz Scores:")
        for score in dashboard['recent_scores']:
            print(f"      - {score['topic']}: {score['score']}/{score['total']} ({score['percentage']:.0f}%)")
    print()
    
    print("=" * 70)
    print("EXAMPLE COMPLETE")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Try different topics")
    print("2. Take multiple quizzes to see difficulty adaptation")
    print("3. Explore the source code in learning_assistant/")
    print("4. Run integration tests: python -m tests.test_agent")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Created .env file with GEMINI_API_KEY")
        print("3. Valid internet connection for Wikipedia API")
        print()
        raise
