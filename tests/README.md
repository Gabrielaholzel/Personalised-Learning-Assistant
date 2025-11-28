# Tests

This directory contains integration tests for the Personalised Learning Assistant.

## Running Tests

```bash
# Run all integration tests
python -m tests.test_agent
```

## Test Coverage

The integration tests cover:

1. **Learning Package Creation**
   - Creates a complete learning package for a test topic
   - Verifies all components are present (research, plan, quiz)
   - Checks data structure integrity

2. **Quiz Evaluation**
   - Simulates user answers
   - Evaluates quiz performance
   - Verifies progress tracking and difficulty adaptation

3. **User Dashboard**
   - Retrieves user progress summary
   - Verifies all metrics are calculated correctly
   - Checks recommendation generation

## Expected Output

When tests pass, you should see:

```
🧪 RUNNING INTEGRATION TESTS
============================================================

TEST: Create Learning Package
============================================================

📚 Creating learning package for 'Python Programming'...
🎯 Goal: Learn basic Python syntax and concepts
📊 Difficulty Level: BEGINNER

🔍 Step 1: Researching topic...
✓ Research complete

📝 Step 2: Generating learning plan (Difficulty: beginner)...
✓ Learning plan generated

❓ Step 3: Creating 3-question quiz...
✓ Quiz created (3 questions)

✅ Learning package complete!

✅ TEST PASSED: Learning package created successfully

...

============================================================
✅ ALL TESTS PASSED
============================================================
```

## Test Configuration

Tests use:
- User ID: `test_user`
- Topic: `Python Programming`
- Goal: `Learn basic Python syntax and concepts`
- Quiz Questions: 3 (for faster testing)

## Troubleshooting

If tests fail:

1. **API Key Error**: Ensure `GEMINI_API_KEY` is set in `.env` file
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Wikipedia Errors**: Check internet connection
4. **Rate Limiting**: Wait a few minutes between test runs

## Adding New Tests

To add new tests, create functions in `test_agent.py` following this pattern:

```python
def test_new_feature():
    """Test description."""
    print("=" * 60)
    print("TEST: New Feature")
    print("=" * 60)
    print()
    
    try:
        # Test code here
        assert condition, "Error message"
        
        print("✅ TEST PASSED: Description")
        return result
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        raise
```

Then add to `run_all_tests()`:

```python
def run_all_tests():
    # ... existing tests ...
    test_new_feature()
```
