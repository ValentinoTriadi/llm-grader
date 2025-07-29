# Code Grading System - Prompt Engineering for LLM-based Code Evaluation

This system provides comprehensive prompt engineering tools for evaluating student code submissions using Large Language Models (LLMs). It includes multiple evaluation styles, detailed rubrics, and structured output formats.

## Features

### 📊 Multiple Evaluation Styles

- **Quick Evaluation**: Fast assessment for basic grading
- **Comprehensive Analysis**: Detailed evaluation with full rubric
- **JSON Format**: Structured output for automated processing
- **Teaching Assistant Style**: Simple issue identification
- **Debug-Focused**: Emphasis on error identification and fixes
- **Industry Standards**: Professional code review approach
- **Algorithm Analysis**: Deep dive into algorithmic efficiency

### 🎯 Evaluation Metrics (100 points total)

Based on comprehensive rubric covering:

- **Correctness (40 points)**
  - Test case coverage (20 pts)
  - Edge case handling (10 pts)
  - Syntax errors (5 pts)
  - Logical accuracy (5 pts)

- **Efficiency (27 points)**
  - Time complexity (11 pts)
  - Optimal algorithms (10 pts)
  - Space complexity (6 pts)

- **Data Structures (15 points)**
  - Appropriate selection (8 pts)
  - Efficient usage (7 pts)

- **Code Readability (10 points)**
  - Documentation (4 pts)
  - Modularity (3 pts)
  - Naming conventions (3 pts)

- **Testing (8 points)**
  - Test design (4 pts)
  - Debugging practices (2 pts)
  - Error handling (2 pts)

## Quick Start

### 🚀 Easy Setup (Recommended)

```python
from easy_setup import EasySetup

# Interactive setup wizard
setup = EasySetup()
setup.interactive_setup()

# Grade code
result = setup.grade_single(
    problem="Write a function to reverse a string",
    code="def reverse_string(s): return s[::-1]",
    evaluation_type="json"
)
print(f"Grade: {result['grade']}/100")
```

### Manual Setup

```python
from client_manager import ClientManager
from main import CodeGradingApp

# Initialize with your preferred model
client_manager = ClientManager()
app = CodeGradingApp(client_manager.get_client("gemini"))

# Generate evaluation
result = app.json_grade(
    problem="Write a function to reverse a string",
    solution="def reverse_string(s): return s[::-1]"
)
```

## Model Integration

### 🆓 Free Options

- **Ollama** (Completely free, runs locally)
  - Models: Llama 3.1, Mistral, CodeLlama, Phi-3, Gemma
  - Setup: Install Ollama, then `ollama pull llama3.1`
  
- **Google Gemini** (Generous free tier)
  - Models: Gemini 1.5 Flash, Gemini 1.5 Pro
  - Setup: Get API key from Google AI Studio
  
- **Groq** (Fast inference, free tier)
  - Models: Llama 3.1, Mixtral, Gemma
  - Setup: Get API key from Groq Console

### 💰 Paid Options

- **OpenAI** (GPT-4, GPT-3.5-turbo)
- **Anthropic** (Claude 3.5 Sonnet, Claude 3 Haiku)

## File Structure

```
├── main.py                 # Main application interface
├── easy_setup.py          # Easy setup wizard and utilities
├── client_manager.py      # LLM client management
├── grading_system.py      # Core grading system with prompts
├── json_evaluator.py      # JSON-formatted evaluation prompts
├── prompt_templates.py    # Specialized prompt templates
├── batch_grader.py        # Batch processing utilities
├── clients/               # LLM client implementations
│   ├── __init__.py
│   ├── ollama_client.py
│   ├── gemini_client.py
│   ├── groq_client.py
│   ├── openai_client.py
│   └── anthropic_client.py
├── examples/              # Example usage scripts
└── README.md             # This documentation
```

## Usage Examples

### 1. Interactive Setup

```bash
python easy_setup.py
```

Follow the prompts to configure your preferred LLM provider.

### 2. Batch Grading

```python
from batch_grader import BatchGrader

grader = BatchGrader("gemini")  # or "ollama", "groq", etc.

# Grade multiple submissions
submissions = [
    {"problem": "Sort array", "code": "def sort(arr): return sorted(arr)"},
    {"problem": "Find max", "code": "def find_max(arr): return max(arr)"}
]

results = grader.grade_batch(submissions, evaluation_type="json")
```

### 3. Single Code Evaluation

```python
from easy_setup import EasySetup

setup = EasySetup()
setup.setup_gemini("YOUR_API_KEY")

result = setup.grade_single(
    problem="Implement binary search",
    code=student_code,
    evaluation_type="comprehensive"
)
```

### 4. Custom Configuration

```python
from client_manager import ClientManager
from main import CodeGradingApp

# Custom client setup
client_manager = ClientManager()
client = client_manager.get_client("ollama", model="llama3.1")
app = CodeGradingApp(client)

# Use different evaluation styles
quick_result = app.quick_grade(problem, solution)
json_result = app.json_grade(problem, solution)
comprehensive_result = app.comprehensive_grade(problem, solution)
```

## Evaluation Types

### Quick Evaluation
Fast assessment with basic feedback and numerical score.

### Comprehensive Analysis
Detailed evaluation with full rubric breakdown, explanations, and improvement suggestions.

### JSON Format
Structured output perfect for automated processing:

```json
{
    "evaluation_summary": {
        "total_score": 85,
        "percentage": 85.0,
        "is_correct": true,
        "grade_letter": "B+"
    },
    "detailed_scores": {
        "correctness": {"score": 35, "max": 40},
        "efficiency": {"score": 22, "max": 27},
        "data_structures": {"score": 13, "max": 15},
        "readability": {"score": 8, "max": 10},
        "testing": {"score": 7, "max": 8}
    },
    "feedback": "Well-structured solution with good performance...",
    "improvements": ["Consider edge case handling", "Add input validation"]
}
```

### Teaching Assistant Style
Simple issue identification with line-specific hints.

### Debug-Focused
Emphasis on error identification and specific fixes.

## Advanced Features

### Algorithm Analysis
Deep dive into time/space complexity and algorithmic efficiency.

### Industry Standards
Professional code review with best practices evaluation.

### Comparative Analysis
Compare multiple solutions side-by-side.

### Custom Rubrics
Define your own evaluation criteria and weights.

## Configuration

### Environment Variables
```bash
# Optional: Set default API keys
export OPENAI_API_KEY="your_key_here"
export GOOGLE_API_KEY="your_key_here"
export GROQ_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"
```

### Model Selection
Each client supports multiple models:
- **Ollama**: llama3.1, mistral, codellama, phi3, gemma
- **Gemini**: gemini-1.5-flash, gemini-1.5-pro
- **OpenAI**: gpt-4, gpt-3.5-turbo
- **Groq**: llama-3.1-70b-versatile, mixtral-8x7b-32768

## Best Practices

1. **Start with Easy Setup**: Use the interactive wizard for quick configuration
2. **Choose Appropriate Models**: Balance cost, speed, and accuracy
3. **Use JSON Format**: For automated grading and integration
4. **Batch Processing**: For multiple submissions
5. **Local Models**: Consider Ollama for privacy and cost-effectiveness

## Error Handling

The system includes comprehensive error handling for:
- Network connectivity issues
- API rate limits
- Invalid responses
- Model unavailability

## Contributing

To contribute:
1. Add new client implementations in `clients/`
2. Extend evaluation methods in prompt templates
3. Add new features to the main application
4. Update documentation and examples

## License

MIT License - Feel free to use and modify for educational purposes.
