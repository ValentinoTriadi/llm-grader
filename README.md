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

```python
from main import CodeGradingApp

app = CodeGradingApp()

# Basic usage
problem = "Write a function to reverse a string"
solution = "def reverse_string(s): return s[::-1]"

# Generate different types of prompts
quick_prompt = app.quick_grade(problem, solution)
comprehensive_prompt = app.comprehensive_grade(problem, solution)
json_prompt = app.json_grade(problem, solution)
```

## File Structure

- `main.py` - Main application interface
- `grading_system.py` - Core grading system with comprehensive prompts
- `json_evaluator.py` - JSON-formatted evaluation prompts
- `prompt_templates.py` - Specialized prompt templates
- `README.md` - This documentation

## Example Usage

### 1. Quick Evaluation

```python
prompt = app.quick_grade(
    problem="Find the maximum element in an array",
    solution="def find_max(arr): return max(arr)"
)
```

### 2. Comprehensive with Model Solution

```python
prompt = app.comprehensive_grade(
    problem="Implement binary search",
    solution=student_code,
    model_solution=reference_code
)
```

### 3. JSON Format for Automation

```python
prompt = app.json_grade(problem, solution)
# Returns structured JSON response for automated processing
```

### 4. Custom Rubric

```python
custom_rubric = {
    "Functionality": {"weight": 50, "criteria": ["Works correctly", "Handles edge cases"]},
    "Style": {"weight": 30, "criteria": ["Good naming", "Clear structure"]},
    "Efficiency": {"weight": 20, "criteria": ["Good performance", "Optimal approach"]}
}

prompt = app.custom_rubric_grade(problem, solution, custom_rubric)
```

## Prompt Types

### Teaching Assistant Style

Simple JSON format for identifying specific issues:

```json
{
  "is_correct": false,
  "hints": [
    {
      "line_number": 3,
      "code_line": "x = x + 2",
      "hint": "Variable 'x' used before initialization"
    }
  ]
}
```

### Comprehensive JSON

Detailed structured evaluation:

```json
{
    "evaluation_summary": {
        "total_score": 85,
        "percentage": 85.0,
        "is_correct": true
    },
    "detailed_scores": {
        "correctness": {"score": 35, "max": 40, "feedback": "..."},
        "efficiency": {"score": 22, "max": 27, "feedback": "..."}
    },
    "issues_found": [...],
    "recommendations": {...}
}
```

## Advanced Features

### Comparative Evaluation

Compare multiple student solutions:

```python
solutions = [
    {"name": "Student A", "code": code_a},
    {"name": "Student B", "code": code_b}
]
prompt = app.compare_solutions(problem, solutions)
```

### Algorithm Analysis

Deep algorithmic evaluation:

```python
prompt = app.algorithm_analysis_grade(
    problem=problem,
    solution=solution,
    expected_complexity="O(n log n) time, O(1) space"
)
```

### Industry Standards Review

Professional code review approach:

```python
prompt = app.industry_standards_grade(problem, solution)
```

## System Prompts

The system includes carefully crafted system prompts for different contexts:

- **Comprehensive**: Detailed academic evaluation
- **Quick**: Fast but thorough assessment
- **Professional**: Industry-standard code review

## Best Practices

1. **Choose the Right Prompt Type**: Match the evaluation style to your needs
2. **Provide Context**: Include problem descriptions and expectations
3. **Use Model Solutions**: When available, include reference implementations
4. **Customize Rubrics**: Adapt scoring criteria to your course requirements
5. **Structured Output**: Use JSON formats for automated processing

## Model Integration

The system includes ready-to-use model clients for popular free and paid APIs:

### 🆓 Free Options

- **Ollama** (Completely free, runs locally)
  - Models: Llama 3, Mistral, CodeLlama, Phi-3, Gemma
  - Setup: Install Ollama, then `ollama pull llama3`
- **Google Gemini** (Generous free tier)
  - Models: Gemini 1.5 Flash, Gemini 1.5 Pro
  - Setup: Get API key from Google AI Studio
- **Groq** (Fast inference, free tier)
  - Models: Llama 3, Mixtral, Gemma
  - Setup: Get API key from Groq Console
- **Hugging Face** (Free tier available)
  - Many open-source models
  - Setup: Get API key from Hugging Face

### 🚀 Quick Start

```python
from easy_setup import EasySetup

# Option 1: Gemini (recommended for best results)
setup = EasySetup()
setup.setup_gemini("YOUR_API_KEY")

# Option 2: Ollama (completely free)
setup = EasySetup()
setup.setup_ollama("llama3")

# Grade code
result = setup.grade_single(
    problem="Write a function to sort a list",
    code="def sort_list(lst): return sorted(lst)",
    evaluation_type="json"
)
print(f"Grade: {result['grade']}/100")
```

### 📋 Easy Setup Wizard

```python
python easy_setup.py
```

This will guide you through setting up your preferred model provider with an interactive wizard.

## Integration with LLMs

These prompts are designed to work with various LLM providers:

- OpenAI GPT-4/GPT-3.5
- Anthropic Claude
- Google Gemini
- Local models (Llama, Mistral, etc.)

Simply send the generated prompt to your chosen LLM API for evaluation.

## Contributing

To add new prompt templates or evaluation criteria:

1. Add new methods to `PromptTemplateLibrary`
2. Update the `CodeGradingApp` interface
3. Add examples and documentation

## License

MIT License - Feel free to use and modify for educational purposes.
