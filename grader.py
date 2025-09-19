"""
Code Grading System - Single Entry Point
Simple, clean interface for grading student code using multiple AI providers
"""

import json, os, dotenv
from typing import Dict, Any, Optional, List

from src.engine.grading_engine import GradingEngine, GradingResult


class CodeGrader:
    """
    Main entry point for the code grading system.
    Supports multiple AI providers: OpenAI, Anthropic, Groq, and Gemini.
    """

    def __init__(
        self, api_key: str, model: str = "gpt-3.5-turbo", provider: str = "openai"
    ):
        """
        Initialize the code grader.

        Args:
            api_key: Your AI provider API key
            model: Model to use (depends on provider)
            provider: AI provider ("openai", "anthropic", "groq", "gemini")

        Popular free/cheap options:
            - OpenAI: "gpt-3.5-turbo" (cheap, reliable)
            - Groq: "llama3-8b-8192" (free, very fast)
            - Groq: "mixtral-8x7b-32768" (free, good quality)
            - Anthropic: "claude-3-haiku-20240307" (cheap)
            - Gemini: "gemini-1.5-flash" (free tier)
        """
        self.engine = GradingEngine(api_key, model, provider)
        self.provider = provider
        self._test_connection()

    def _test_connection(self):
        """Test API connection on initialization"""
        if not self.engine.test_connection():
            raise ConnectionError(
                f"Failed to connect to {self.provider} API. Please check your API key and internet connection."
            )

    def grade_code(
        self,
        problem: str,
        student_code: str,
        student_id: str = "student",
        format: str = "json",
        model_solution: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Grade a single code submission.

        Args:
            problem: The programming problem description
            student_code: The student's code solution
            student_id: Optional student identifier
            format: Response format ("json", "simple", or "comprehensive")
            model_solution: Optional reference solution for comparison

        Returns:
            Dictionary with grading results
        """

        result = self.engine.grade_code(
            student_id=student_id,
            problem=problem,
            code=student_code,
            evaluation_type=format,
            model_solution=model_solution,
        )

        return self._format_result(result)

    def grade_multiple(
        self, submissions: List[Dict[str, str]], format: str = "json"
    ) -> List[Dict[str, Any]]:
        """
        Grade multiple code submissions.

        Args:
            submissions: List of dictionaries with 'problem', 'code', and optional 'student_id'
            format: Response format ("json", "simple", or "comprehensive")

        Returns:
            List of grading results
        """

        results = self.engine.grade_batch(submissions, format)
        return [self._format_result(result) for result in results]

    def _format_result(self, result: GradingResult) -> Dict[str, Any]:
        """Format result for external use"""

        return {
            "student_id": result.student_id,
            "success": result.success,
            "grade": result.grade,
            "percentage": result.percentage,
            "feedback": result.feedback,
            "issues": result.issues or [],
            "recommendations": result.recommendations or [],
            "strengths": result.strengths or [],
            "processing_time": result.processing_time,
            "error": result.error_message,
        }

    def get_prompt_only(
        self,
        problem: str,
        student_code: str,
        format: str = "json",
        model_solution: Optional[str] = None,
    ) -> str:
        """
        Generate just the prompt without calling the API.
        Useful for manual evaluation or debugging.

        Args:
            problem: The programming problem description
            student_code: The student's code solution
            format: Prompt format ("json", "simple", or "comprehensive")
            model_solution: Optional reference solution

        Returns:
            The generated prompt string
        """

        if format == "json":
            return self.engine.prompt_generator.generate_json_prompt(
                problem, student_code, model_solution
            )
        elif format == "simple":
            return self.engine.prompt_generator.generate_simple_prompt(
                problem, student_code
            )
        elif format == "comprehensive":
            return self.engine.prompt_generator.generate_comprehensive_prompt(
                problem, student_code, model_solution
            )
        else:
            return self.engine.prompt_generator.generate_json_prompt(
                problem, student_code, model_solution
            )


# Convenience functions for quick usage
def quick_grade(
    api_key: str,
    problem: str,
    code: str,
    format: str = "json",
    model: str = "gpt-3.5-turbo",
    provider: str = "openai",
) -> Dict[str, Any]:
    """
    Quick grade a single submission.

    Args:
        api_key: AI provider API key
        problem: Problem description
        code: Student code
        format: Response format
        model: AI model to use
        provider: AI provider ("openai", "anthropic", "groq", "gemini")

    Returns:
        Grading result dictionary
    """
    grader = CodeGrader(api_key, model, provider)
    return grader.grade_code(problem, code, format=format)


def get_prompt(problem: str, code: str, format: str = "json") -> str:
    """
    Get just the evaluation prompt without API call.

    Args:
        problem: Problem description
        code: Student code
        format: Prompt format

    Returns:
        Generated prompt string
    """
    # Create a dummy grader just for prompt generation
    from src.prompts.generator import PromptGenerator

    generator = PromptGenerator()

    if format == "json":
        return generator.generate_json_prompt(problem, code)
    elif format == "simple":
        return generator.generate_simple_prompt(problem, code)
    elif format == "comprehensive":
        return generator.generate_comprehensive_prompt(problem, code)
    else:
        return generator.generate_json_prompt(problem, code)


def main(problem: str = None, student_code: str = None, detailed: bool = False):
    print("🎓 Code Grading System")
    print("=" * 50)

    # You need to set your Gemini API key here
    # Load environment variables from .env file
    dotenv.load_dotenv()
    API_KEY = os.getenv("API_KEY", "YOUR_API_KEY_HERE")

    if API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Please set your Gemini API key in the code")
        print("Get one free at: https://makersuite.google.com/app/apikey")

        # Show prompt generation without API
        print("\n📋 Example: Prompt Generation (No API needed)")

        prompt = get_prompt(problem, student_code, "json")
        print(f"Generated prompt length: {len(prompt)} characters")
        print("You can copy this prompt to ChatGPT or any LLM!")

    else:
        try:
            # TODO: ADJUST THIS TO YOUR PREFERRED MODEL
            grader = CodeGrader(API_KEY, model="gemini-2.5-pro", provider="gemini")

            result = grader.grade_code(
                problem=problem
                or "Write a function to find the maximum element in a list",
                student_code=student_code
                or """
def find_max(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val
""",
                format="json",
            )

            print("✅ Grading successful!")
            print(f"Grade: {result['grade']}/100")
            print(f"Issues found: {len(result['issues'])}")
            print("Feedback:")
            for issue in result["issues"][:3]:  # Show first 3 issues
                print(f"  - {issue.get('description', issue)}")

            if detailed:
                return
            print(f"Student ID: {result['student_id']}")
            print(f"Success: {result['success']}")
            print(f"Percentage: {result['percentage']}%")
            print(f"Processing time: {result['processing_time']}s")

            if result["feedback"]:
                print(f"\Components:")
                correctness = result["feedback"]["category_scores"].get(
                    "correctness", "N/A"
                )
                efficiency = result["feedback"]["category_scores"].get(
                    "efficiency", "N/A"
                )
                data_structures = result["feedback"]["category_scores"].get(
                    "data_structures", "N/A"
                )
                code_quality = result["feedback"]["category_scores"].get(
                    "code_quality", "N/A"
                )
                testing = result["feedback"]["category_scores"].get("testing", "N/A")
                print(
                    f"    Correctness: {correctness.get('score', 'N/A')}/{correctness.get('max', 'N/A')}.  {correctness.get('feedback', 'N/A')}"
                )
                print(
                    f"    Efficiency: {efficiency.get('score', 'N/A')}/{efficiency.get('max', 'N/A')}.  {efficiency.get('feedback', 'N/A')}"
                )
                print(
                    f"    Data Structures: {data_structures.get('score', 'N/A')}/{data_structures.get('max', 'N/A')}.  {data_structures.get('feedback', 'N/A')}"
                )
                print(
                    f"    Code Quality: {code_quality.get('score', 'N/A')}/{code_quality.get('max', 'N/A')}.  {code_quality.get('feedback', 'N/A')}"
                )
                print(
                    f"    Testing: {testing.get('score', 'N/A')}/{testing.get('max', 'N/A')}.  {testing.get('feedback', 'N/A')}"
                )

            if result["recommendations"]:
                print(f"\nRecommendations:")
                for rec in result["recommendations"]:
                    print(f"  - {rec}")

            if result["strengths"]:
                print(f"\nStrengths:")
                for strength in result["strengths"]:
                    print(f"  - {strength}")

            if result["error"]:
                print(f"\nError: {result['error']}")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("Check your API key and internet connection")


if __name__ == "__main__":
    sample_problem = "Write a function to find the maximum element in a list"
    sample_code = """
def find_max(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val
"""
    main(sample_problem, sample_code)
