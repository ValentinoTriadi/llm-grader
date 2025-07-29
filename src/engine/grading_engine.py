"""
Code Grading Engine
Main processing engine that coordinates prompt generation and API calls
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from .grading_client import MultiModelClient, GradingResponse
from ..prompts.generator import PromptGenerator


@dataclass
class GradingResult:
    """Complete grading result"""

    student_id: str
    problem: str
    code: str
    success: bool
    grade: Optional[float] = None
    percentage: Optional[float] = None
    feedback: Optional[Dict[str, Any]] = None
    issues: List[Dict[str, Any]] = None
    recommendations: List[str] = None
    strengths: List[str] = None
    processing_time: float = 0.0
    error_message: Optional[str] = None


class GradingEngine:
    """Main engine for code evaluation"""

    def __init__(
        self, api_key: str, model: str = "gpt-3.5-turbo", provider: str = "openai"
    ):
        self.client = MultiModelClient(api_key, model, provider)
        self.prompt_generator = PromptGenerator()

    def grade_code(
        self,
        student_id: str,
        problem: str,
        code: str,
        evaluation_type: str = "json",
        model_solution: Optional[str] = None,
    ) -> GradingResult:
        """Grade a single code submission"""

        # Generate appropriate prompt
        if evaluation_type == "json":
            prompt = self.prompt_generator.generate_json_prompt(
                problem, code, model_solution
            )
        elif evaluation_type == "simple":
            prompt = self.prompt_generator.generate_simple_prompt(problem, code)
        elif evaluation_type == "comprehensive":
            prompt = self.prompt_generator.generate_comprehensive_prompt(
                problem, code, model_solution
            )
        else:
            prompt = self.prompt_generator.generate_json_prompt(
                problem, code, model_solution
            )

        # Get response from Gemini
        response = self.client.evaluate_code(prompt)

        if not response.success:
            return GradingResult(
                student_id=student_id,
                problem=problem,
                code=code,
                success=False,
                processing_time=response.processing_time,
                error_message=response.error_message,
            )

        # Parse response based on evaluation type
        if evaluation_type == "json":
            return self._parse_json_result(student_id, problem, code, response)
        elif evaluation_type == "simple":
            return self._parse_simple_result(student_id, problem, code, response)
        else:
            return self._parse_text_result(student_id, problem, code, response)

    def _parse_json_result(
        self, student_id: str, problem: str, code: str, response: GradingResponse
    ) -> GradingResult:
        """Parse JSON format response"""

        parsed = self.client.parse_json_response(response.raw_response)

        if "error" in parsed:
            return GradingResult(
                student_id=student_id,
                problem=problem,
                code=code,
                success=False,
                processing_time=response.processing_time,
                error_message=f"JSON parsing error: {parsed['error']}",
            )

        # Extract information from JSON response
        grade = parsed.get("total_score", 0)
        percentage = parsed.get("percentage", (grade / 100.0 * 100) if grade else 0)
        issues = parsed.get("issues", [])
        recommendations = parsed.get("recommendations", [])
        strengths = parsed.get("strengths", [])

        return GradingResult(
            student_id=student_id,
            problem=problem,
            code=code,
            success=True,
            grade=grade,
            percentage=percentage,
            feedback=parsed,
            issues=issues,
            recommendations=recommendations,
            strengths=strengths,
            processing_time=response.processing_time,
        )

    def _parse_simple_result(
        self, student_id: str, problem: str, code: str, response: GradingResponse
    ) -> GradingResult:
        """Parse simple teaching assistant style response"""

        parsed = self.client.parse_json_response(response.raw_response)

        if "error" in parsed:
            return GradingResult(
                student_id=student_id,
                problem=problem,
                code=code,
                success=False,
                processing_time=response.processing_time,
                error_message=f"JSON parsing error: {parsed['error']}",
            )

        is_correct = parsed.get("is_correct", False)
        hints = parsed.get("hints", [])

        # Convert to standard format
        grade = 100.0 if is_correct else (50.0 if not hints else 25.0)

        return GradingResult(
            student_id=student_id,
            problem=problem,
            code=code,
            success=True,
            grade=grade,
            percentage=grade,
            feedback=parsed,
            issues=hints,
            processing_time=response.processing_time,
        )

    def _parse_text_result(
        self, student_id: str, problem: str, code: str, response: GradingResponse
    ) -> GradingResult:
        """Parse comprehensive text response"""

        # Try to extract score from text
        text = response.raw_response
        grade = None

        # Look for score patterns
        import re

        score_patterns = [
            r"TOTAL:\s*(\d+)/100",
            r"Total:\s*(\d+)/100",
            r"Score:\s*(\d+)/100",
            r"Grade:\s*(\d+)/100",
        ]

        for pattern in score_patterns:
            match = re.search(pattern, text)
            if match:
                grade = float(match.group(1))
                break

        # Look for percentage if no grade found
        if grade is None:
            percentage_match = re.search(r"(\d+\.?\d*)%", text)
            if percentage_match:
                grade = float(percentage_match.group(1))

        percentage = grade if grade is not None else 0.0

        return GradingResult(
            student_id=student_id,
            problem=problem,
            code=code,
            success=True,
            grade=grade,
            percentage=percentage,
            feedback={"raw_text": text},
            processing_time=response.processing_time,
        )

    def test_connection(self) -> bool:
        """Test the Gemini API connection"""
        result = self.client.test_connection()
        return result.success

    def grade_batch(
        self, submissions: List[Dict[str, Any]], evaluation_type: str = "json"
    ) -> List[GradingResult]:
        """Grade multiple submissions"""

        results = []
        for submission in submissions:
            result = self.grade_code(
                student_id=submission.get("student_id", "unknown"),
                problem=submission["problem"],
                code=submission["code"],
                evaluation_type=evaluation_type,
                model_solution=submission.get("model_solution"),
            )
            results.append(result)

        return results
