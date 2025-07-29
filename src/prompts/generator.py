"""
Prompt Generation Module
Clean separation of prompt engineering logic
"""

from typing import Optional, Dict, Any


class PromptGenerator:
    """Generate evaluation prompts for code grading"""

    def __init__(self):
        self.system_prompt = self._get_system_prompt()
        self.metrics = self._get_metrics()

    def _get_system_prompt(self) -> str:
        """System prompt for the LLM"""
        return """You are an expert computer science professor evaluating student code submissions. 

Your evaluation approach:
- Thorough analysis across multiple dimensions
- Fair and consistent scoring
- Constructive feedback for learning
- Clear justification for scores

Evaluate code on:
1. Correctness (40 pts): Functionality, edge cases, syntax, logic
2. Efficiency (27 pts): Time/space complexity, optimal algorithms  
3. Data Structures (15 pts): Appropriate selection and usage
4. Code Quality (10 pts): Readability, documentation, structure
5. Testing (8 pts): Test design, debugging, error handling

Total: 100 points"""

    def _get_metrics(self) -> str:
        """Detailed scoring rubric"""
        return """
GRADING RUBRIC (100 points total):

CORRECTNESS (40 points):
- Test Case Coverage (20 pts): Passes basic tests (10) + edge cases (10)
- Edge Case Handling (10 pts): Boundary conditions, empty inputs, etc.
- No Syntax Errors (5 pts): Code compiles and runs without errors
- Logical Accuracy (5 pts): Algorithm correctly implements requirements

EFFICIENCY (27 points):
- Time Complexity (11 pts): Meets requirements (6) + analysis in comments (5)
- Optimal Algorithm (10 pts): Best approach (5) + considers optimizations (5)
- Space Complexity (6 pts): Efficient memory usage (3) + avoids waste (3)

DATA STRUCTURES (15 points):
- Structure Selection (8 pts): Appropriate choice (4) + explains rationale (4)
- Usage Efficiency (7 pts): Optimal utilization (4) + performance impact (3)

CODE QUALITY (10 points):
- Documentation (4 pts): Clear comments (2) + function descriptions (2)
- Modularity (3 pts): Functions/modules (2) + single responsibility (1)
- Naming (3 pts): Descriptive names (2) + follows conventions (1)

TESTING (8 points):
- Test Design (4 pts): Creates tests (2) + covers scenarios (2)
- Debugging (2 pts): Systematic approach (1) + documents process (1)
- Error Handling (2 pts): Validates inputs and handles errors
"""

    def generate_json_prompt(
        self, problem: str, student_code: str, model_solution: Optional[str] = None
    ) -> str:
        """Generate JSON format evaluation prompt"""

        model_section = ""
        if model_solution:
            model_section = f"""
## REFERENCE SOLUTION:
```
{model_solution}
```
"""

        return f"""{self.system_prompt}

## PROBLEM:
{problem}
{model_section}
## STUDENT CODE:
```
{student_code}
```

{self.metrics}

## REQUIRED OUTPUT:
Respond with ONLY a valid JSON object in this exact format:

```json
{{
    "total_score": number,
    "percentage": number,
    "is_correct": boolean,
    "category_scores": {{
        "correctness": {{"score": number, "max": 40, "feedback": "string"}},
        "efficiency": {{"score": number, "max": 27, "feedback": "string"}},
        "data_structures": {{"score": number, "max": 15, "feedback": "string"}},
        "code_quality": {{"score": number, "max": 10, "feedback": "string"}},
        "testing": {{"score": number, "max": 8, "feedback": "string"}}
    }},
    "issues": [
        {{
            "line_number": number,
            "description": "string",
            "severity": "critical|major|minor",
            "suggestion": "string"
        }}
    ],
    "strengths": ["string"],
    "recommendations": ["string"],
    "complexity_analysis": {{
        "time_complexity": "string",
        "space_complexity": "string"
    }}
}}
```

Evaluate the code now and respond with only the JSON object."""

    def generate_simple_prompt(self, problem: str, student_code: str) -> str:
        """Generate simple teaching assistant style prompt"""

        return f"""I want you to act as a programming teacher that helps students solve programming assignments.

Review the student's code for the following problem:

Problem: {problem}

Student Code: {student_code}

Identify if the code executes correctly and fulfills the problem's requirements. If not, provide a JSON object with:
- "is_correct": A boolean indicating whether the code is correct.
- "hints": An array of objects, each with:
  - "line_number": The line number of the issue.
  - "code_line": The code line with the issue.
  - "hint": A short explanation of what is wrong.

Example output:
{{
    "is_correct": false,
    "hints": [
        {{
            "line_number": 3,
            "code_line": "x = x + 2",
            "hint": "The variable 'x' is used before being initialized."
        }}
    ]
}}

If the code is correct, return:
{{
    "is_correct": true,
    "hints": []
}}"""

    def generate_comprehensive_prompt(
        self, problem: str, student_code: str, model_solution: Optional[str] = None
    ) -> str:
        """Generate comprehensive text evaluation prompt"""

        model_section = ""
        if model_solution:
            model_section = f"""
## MODEL SOLUTION:
```
{model_solution}
```
"""

        return f"""{self.system_prompt}

## PROBLEM DESCRIPTION:
{problem}
{model_section}
## STUDENT SUBMISSION:
```
{student_code}
```

{self.metrics}

## EVALUATION INSTRUCTIONS:
Provide a comprehensive evaluation including:

1. **FUNCTIONALITY ANALYSIS**
   - Does the code solve the problem correctly?
   - What test cases would it pass/fail?
   - Are there logical errors or bugs?

2. **EFFICIENCY EVALUATION**
   - Time and space complexity analysis
   - Is this optimal for the problem?
   - Suggestions for optimization

3. **CODE QUALITY ASSESSMENT**
   - Readability and maintainability
   - Best practices adherence
   - Areas for improvement

4. **SCORING BREAKDOWN**
   - Correctness: ___/40 points
   - Efficiency: ___/27 points
   - Data Structures: ___/15 points
   - Code Quality: ___/10 points
   - Testing: ___/8 points
   
   **TOTAL: ___/100 points**

5. **RECOMMENDATIONS**
   - Top 3 strengths
   - Top 3 areas for improvement
   - Specific suggestions for enhancement"""
