"""Quiz Agent - Generates adaptive quizzes and evaluates answers."""

import google.generativeai as genai
from typing import Dict, List

from learning_assistant.config import config


class QuizAgent:
    """
    Quiz Agent that generates adaptive multiple-choice questions
    and evaluates user answers with detailed explanations.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialise the Quiz Agent.
        
        Args:
            api_key: Google Gemini API key (optional, uses config if not provided)
        """
        api_key = api_key or config.GEMINI_API_KEY
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
    
    def generate_quiz(self, topic: str, difficulty: str = "beginner", 
                     num_questions: int = 5) -> List[Dict]:
        """
        Generate an adaptive multiple-choice quiz.
        
        Args:
            topic: The topic to create quiz about
            difficulty: Difficulty level (beginner/intermediate/advanced)
            num_questions: Number of questions to generate
            
        Returns:
            List of question dictionaries, each containing:
                - question: The question text
                - options: Dictionary of answer options (A, B, C, D)
                - correct: The correct answer letter
                - explanation: Explanation of why the answer is correct
        """
        difficulty_guidance = {
            "beginner": "Focus on basic concepts and definitions. Questions should test fundamental understanding.",
            "intermediate": "Include application-based questions. Test understanding of how concepts work together.",
            "advanced": "Focus on complex scenarios, edge cases, and expert-level knowledge. Include analytical questions."
        }
        
        guidance = difficulty_guidance.get(difficulty, difficulty_guidance["beginner"])
        
        prompt = f"""Create a {difficulty} level quiz about {topic} with {num_questions} multiple choice questions.

{guidance}

Format each question EXACTLY as follows:

Q1: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct: [A/B/C/D]
Explanation: [Why this answer is correct and why others are wrong]

---

Q2: [Question text]
...

Make questions progressively challenging within the {difficulty} level.
Ensure all options are plausible to test true understanding.
Provide clear, educational explanations."""
        
        response = self.model.generate_content(prompt)
        return self._parse_quiz(response.text)
    
    def _parse_quiz(self, quiz_text: str) -> List[Dict]:
        """
        Parse quiz text into structured format.
        
        Args:
            quiz_text: Raw quiz text from LLM
            
        Returns:
            List of structured question dictionaries
        """
        questions = []
        question_blocks = quiz_text.split('---')
        
        for block in question_blocks:
            if not block.strip():
                continue
            
            lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
            if len(lines) < 6:  # Minimum: question + 4 options + correct + explanation
                continue
            
            question = {
                "question": "",
                "options": {},
                "correct": "",
                "explanation": ""
            }
            
            # Parse question text
            for line in lines:
                if line.startswith(('Q', 'Question')):
                    # Extract question text after the number and colon
                    if ':' in line:
                        question["question"] = line.split(':', 1)[1].strip()
                    else:
                        question["question"] = line
                    break
            
            # Parse options and metadata
            for line in lines:
                if line.startswith(('A)', 'B)', 'C)', 'D)')):
                    key = line[0]
                    value = line[2:].strip()
                    question["options"][key] = value
                elif line.startswith('Correct:'):
                    # Extract just the letter
                    correct_text = line.split(':')[1].strip()
                    question["correct"] = correct_text[0].upper()
                elif line.startswith('Explanation:'):
                    question["explanation"] = line.split(':', 1)[1].strip()
            
            # Only add if we have all required components
            if question["question"] and question["options"] and question["correct"]:
                questions.append(question)
        
        return questions
    
    def evaluate_answer(self, question: Dict, user_answer: str) -> Dict:
        """
        Evaluate a user's answer to a question.
        
        Args:
            question: Question dictionary with correct answer
            user_answer: User's selected answer (A, B, C, or D)
            
        Returns:
            Dictionary containing:
                - correct: Boolean indicating if answer was correct
                - explanation: Explanation from the question
                - correct_answer: The correct answer letter
        """
        is_correct = user_answer.upper() == question["correct"].upper()
        
        return {
            "correct": is_correct,
            "explanation": question.get("explanation", "No explanation available."),
            "correct_answer": question["correct"]
        }
    
    def evaluate_quiz(self, questions: List[Dict], user_answers: Dict[int, str]) -> Dict:
        """
        Evaluate an entire quiz.
        
        Args:
            questions: List of question dictionaries
            user_answers: Dictionary mapping question index to user's answer
            
        Returns:
            Dictionary containing:
                - score: Number of correct answers
                - total: Total number of questions
                - percentage: Score as a percentage
                - results: List of detailed results for each question
        """
        results = []
        score = 0
        
        for i, question in enumerate(questions):
            user_answer = user_answers.get(i, "")
            evaluation = self.evaluate_answer(question, user_answer)
            
            if evaluation["correct"]:
                score += 1
            
            results.append({
                "question_num": i + 1,
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": evaluation["correct_answer"],
                "is_correct": evaluation["correct"],
                "explanation": evaluation["explanation"]
            })
        
        return {
            "score": score,
            "total": len(questions),
            "percentage": (score / len(questions)) * 100 if questions else 0,
            "results": results
        }
