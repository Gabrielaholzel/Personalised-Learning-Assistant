# 🚀 Getting Started with Personalised Learning Assistant

## Quick Setup (5 Minutes)

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### 2. Installation Steps

```bash
# Clone or download this repository
cd personalised-learning-assistant

# Install required packages
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

### 4. Run the Application

**Option A: Python Module**
```bash
python -m learning_assistant.orchestrator
```

**Option B: Integration Tests**
```bash
python -m tests.test_agent
```

**Option C: Jupyter Notebook**
```bash
jupyter notebook personalised-learning-assistant.ipynb
```

## 📚 What's Included

### Main Package
- **learning_assistant/**: Main Python package
  - `orchestrator.py`: Main workflow coordinator
  - `agents/`: Individual agent implementations
  - `config.py`: Configuration settings
  - `tools.py`: Utility functions

### Supporting Files
- **tests/**: Integration tests
- **docs/**: Additional documentation
- **requirements.txt**: Python dependencies
- **.env.example**: Environment configuration template
- **README.md**: Project overview

## 🎯 First Steps

### Run Integration Tests

```bash
python -m tests.test_agent
```

This will:
1. Create a learning package for "Python Programming"
2. Evaluate a quiz with perfect scores
3. Display user dashboard

### Sample Topics to Test

**Beginner-Friendly:**
- "Solar System Basics"
- "How Plants Grow"
- "Introduction to Music"

**Intermediate:**
- "Climate Change Science"
- "Human Body Systems"
- "Photography Fundamentals"

**Advanced:**
- "Quantum Mechanics"
- "Artificial Intelligence"
- "Molecular Biology"

## 🔍 Understanding the System

### How It Works

1. **User enters a topic** (e.g., "Machine Learning")
2. **Research Agent** fetches Wikipedia information
3. **Content Agent** generates a personalised learning plan
4. **Quiz Agent** creates adaptive questions
5. **User takes the quiz**
6. **Personalisation Engine** tracks progress and adjusts difficulty
7. **System adapts** to user's performance level

### Difficulty Levels

- **Beginner**: < 70% average quiz score
- **Intermediate**: 70-84% average quiz score
- **Advanced**: ≥ 85% average quiz score

## 🎓 Learning from the Code

This project demonstrates:

### ADK Course Concepts
- **Day 1**: Multi-agent architecture
- **Day 2**: Agent tools and functions
- **Day 3**: Session and memory management
- **Day 4**: Observability and evaluation
- **Day 5**: Integration and deployment

### Python Best Practices
- Type hints for clarity
- Docstrings for documentation
- Error handling
- Modular design
- Clean code structure

## 🛠️ Customisation

### Change Quiz Length

Modify in `config.py`:
```python
DEFAULT_NUM_QUESTIONS = 10  # Changed from 5
```

### Adjust Difficulty Thresholds

Modify in `config.py`:
```python
ADVANCED_THRESHOLD = 90  # Changed from 85
INTERMEDIATE_THRESHOLD = 75  # Changed from 70
```

### Add New Data Sources

Extend `ResearchAgent` in `agents/research_agent.py` to include:
- arXiv for academic papers
- Khan Academy API
- YouTube educational content

## 🐛 Troubleshooting

### Common Issues

**"No module named 'google.generativeai'"**
```bash
pip install google-generativeai
```

**"GEMINI_API_KEY not found"**
- Check your `.env` file exists
- Verify the API key is correct
- Ensure no extra spaces in the key

**"Wikipedia module not found"**
```bash
pip install wikipedia-api
```

**API Rate Limit Exceeded**
- Wait a few minutes between requests
- Consider using a different API key
- Reduce the number of questions per quiz

## 📖 Next Steps

1. **Run Tests**: Execute integration tests to verify setup
2. **Try Different Topics**: Test with various subjects
3. **Track Progress**: Take multiple quizzes to see adaptation
4. **Customise**: Modify configuration to fit your needs
5. **Extend**: Add new features or agents

## 🤝 Getting Help

- **Code Issues**: Check docstrings in source files
- **Concept Questions**: Review the ADK course concepts section
- **API Problems**: Verify your API key and check quotas
- **General Help**: Review the main README.md

## 🎉 You're Ready!

Start with the integration tests, experiment with different topics, and watch the system adapt to your learning style. Happy learning! 🚀

---

**Need more details?** Check the main [README.md](../README.md) for comprehensive documentation.
