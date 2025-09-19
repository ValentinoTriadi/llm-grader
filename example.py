"""
Example: How to use the Code Grading System
Simple examples showing the single entry point usage
"""

import sys
import os
from grader import main


def run_main_with_input(problem, code, student_id="student"):
    """Helper function to run main function from grader.py with given problem and code"""
    try:
        print(f"--- Results for {student_id} ---")

        # Call main function directly with problem and code
        success = main(problem, code, True)

        print("-" * 40)
        return success

    except Exception as e:
        print(f"Error running main function for {student_id}: {e}")
        print("-" * 40)
        return False


def example_1_basic_usage():
    """Example 1: Basic code grading"""
    print("=== EXAMPLE 1: Basic Usage ===")

    problem = "Write a function to check if a number is even"
    code = """def is_even(n):
  return n % 2 == 0"""

    run_main_with_input(problem, code, "alice")


def example_2_different_problems():
    """Example 2: Different problems and solutions"""
    print("\n=== EXAMPLE 2: Different Problems ===")

    problems_and_solutions = [
        {
            "student": "bob",
            "problem": "Write a function to reverse a string",
            "code": "def reverse(s): return s[::-1]",
        },
        {
            "student": "charlie",
            "problem": "Write a function to calculate factorial",
            "code": """def factorial(n):
  if n <= 1:
    return 1
  return n * factorial(n-1)""",
        },
        {
            "student": "diana",
            "problem": "Write a function to find the maximum number in a list",
            "code": "def find_max(lst): return max(lst) if lst else None",
        },
    ]

    for item in problems_and_solutions:
        run_main_with_input(item["problem"], item["code"], item["student"])


def example_3_same_problem_different_solutions():
    """Example 3: Same problem, different implementations"""
    print("\n=== EXAMPLE 3: Same Problem, Different Solutions ===")

    problem = "Write a function to find the sum of all even numbers in a list"

    solutions = [
        {
            "student": "alice_v1",
            "code": """def sum_evens(lst):
  total = 0
  for num in lst:
    if num % 2 == 0:
      total += num
  return total""",
        },
        {
            "student": "bob_v1",
            "code": "def sum_evens(lst): return sum(x for x in lst if x % 2 == 0)",
        },
        {
            "student": "charlie_v1",
            "code": """def sum_evens(lst):
  return sum(filter(lambda x: x % 2 == 0, lst))""",
        },
        {
            "student": "diana_v1",
            "code": """def sum_evens(lst):
  evens = []
  for num in lst:
    if num % 2 == 0:
      evens.append(num)
  return sum(evens)""",
        },
    ]

    for solution in solutions:
        run_main_with_input(problem, solution["code"], solution["student"])


def example_4_complex_problems():
    """Example 4: More complex programming problems"""
    print("\n=== EXAMPLE 4: Complex Problems ===")

    complex_problems = [
        {
            "student": "expert_1",
            "problem": "Implement binary search on a sorted array",
            "code": """def binary_search(arr, target):
  left, right = 0, len(arr) - 1
  
  while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target:
      return mid
    elif arr[mid] < target:
      left = mid + 1
    else:
      right = mid - 1
  
  return -1""",
        },
        {
            "student": "expert_2",
            "problem": "Write a function to merge two sorted lists",
            "code": """def merge_sorted(list1, list2):
  result = []
  i = j = 0
  
  while i < len(list1) and j < len(list2):
    if list1[i] <= list2[j]:
      result.append(list1[i])
      i += 1
    else:
      result.append(list2[j])
      j += 1
  
  result.extend(list1[i:])
  result.extend(list2[j:])
  return result""",
        },
        {
            "student": "expert_3",
            "problem": "Implement a function to detect if a linked list has a cycle",
            "code": """def has_cycle(head):
  if not head or not head.next:
    return False
  
  slow = head
  fast = head.next
  
  while fast and fast.next:
    if slow == fast:
      return True
    slow = slow.next
    fast = fast.next.next
  
  return False""",
        },
    ]

    for item in complex_problems:
        run_main_with_input(item["problem"], item["code"], item["student"])


def example_5_buggy_code():
    """Example 5: Code with bugs for testing"""
    print("\n=== EXAMPLE 5: Buggy Code Examples ===")

    buggy_examples = [
        {
            "student": "buggy_1",
            "problem": "Write a function to calculate fibonacci numbers",
            "code": """def fibonacci(n):
  if n <= 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fibonacci(n-1) + fibonacci(n-2)""",  # Works but inefficient
        },
        {
            "student": "buggy_2",
            "problem": "Write a function to check if a string is a palindrome",
            "code": """def is_palindrome(s):
  return s == s[::-1]""",  # Doesn't handle case/spaces
        },
        {
            "student": "buggy_3",
            "problem": "Write a function to find all prime numbers up to n",
            "code": """def find_primes(n):
  primes = []
  for i in range(2, n):
    is_prime = True
    for j in range(2, i):
      if i % j == 0:
        is_prime = False
        break
    if is_prime:
      primes.append(i)
  return primes""",  # Inefficient but works
        },
    ]

    for item in buggy_examples:
        run_main_with_input(item["problem"], item["code"], item["student"])


if __name__ == "__main__":
    print("🎓 Code Grading System - Examples with grader.py")
    print("=" * 50)

    # Check if grader.py exists
    if not os.path.exists("grader.py"):
        print("❌ grader.py not found in current directory")
        print("Please make sure grader.py is in the same directory as this script")
        sys.exit(1)

    print("✅ grader.py found! Running examples...")

    try:
        example_1_basic_usage()
        example_2_different_problems()
        example_3_same_problem_different_solutions()
        example_4_complex_problems()
        example_5_buggy_code()

        print("\n🎉 All examples completed!")

    except KeyboardInterrupt:
        print("\n⚠️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

    print("\n📚 Usage Summary:")
    print(
        "This script calls the main function from grader.py with different problems and code samples"
    )
    print("Each example shows how the grader handles various scenarios")
