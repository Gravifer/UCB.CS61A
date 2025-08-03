#!/usr/bin/env python3
"""Test the fully trampolined CPS evaluator."""

import os
import sys

# Add the project directory to the path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)
sys.path.append(os.path.join(project_dir, "scheme_reader"))

from scheme_eval_apply import scheme_eval_cps_fully_trampolined
from scheme_reader import scheme_read, Buffer, InputReader
from scheme_utils import create_global_frame
from scheme_forms import FormatError
from pair import Pair, nil
import traceback

def read_expr(expr_str):
    """Read a Scheme expression from a string."""
    src = Buffer(InputReader(expr_str + '\n'))
    return scheme_read(src)

def test_expression(expr_str, description=""):
    """Test a single expression with the fully trampolined evaluator."""
    print(f"\n=== {description} ===")
    print(f"Testing: {expr_str}")
    try:
        expr = read_expr(expr_str)
        env = create_global_frame()
        result = scheme_eval_cps_fully_trampolined(expr, env)
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return None

def main():
    print("Testing Fully Trampolined CPS Evaluator")
    print("=" * 50)
    
    # Test basic arithmetic
    test_expression("5", "Basic number")
    test_expression("(+ 1 2)", "Simple addition")
    test_expression("(* (+ 1 2) (- 4 1))", "Nested arithmetic")
    
    # Test factorial
    test_expression("""
    (begin
      (define (factorial n)
        (if (< n 1)
            1
            (* n (factorial (- n 1)))))
      (factorial 5))
    """, "Factorial 5")
    
    # Test small countdown
    test_expression("""
    (begin
      (define (countdown n)
        (if (< n 1)
            0
            (countdown (- n 1))))
      (countdown 10))
    """, "Countdown 10")
    
    # Test larger countdown (this should work without stack overflow)
    print("\n=== Critical Test: Deep Recursion ===")
    print("Testing countdown(100) - this should work without stack overflow...")
    try:
        expr_str = """
        (begin
          (define (countdown n)
            (if (< n 1)
                0
                (countdown (- n 1))))
          (countdown 100))
        """
        expr = read_expr(expr_str)
        env = create_global_frame()
        result = scheme_eval_cps_fully_trampolined(expr, env)
        print(f"SUCCESS! countdown(100) = {result}")
    except RecursionError as e:
        print(f"FAILED: Still hitting recursion limit: {e}")
    except Exception as e:
        print(f"FAILED: Other error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
