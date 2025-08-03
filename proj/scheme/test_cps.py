#!/usr/bin/env python3

"""Test script to compare original vs CPS evaluation"""

import sys
import os

sys.path.append("scheme_reader")

from scheme_eval_apply import *
from scheme_reader import *
from scheme_classes import *
from scheme import create_global_frame

def test_basic_arithmetic():
    """Test basic arithmetic with both evaluators"""
    env = create_global_frame()
    
    # Test expression: (+ 1 2 3)
    expr = read_line("(+ 1 2 3)")
    
    print("Testing: (+ 1 2 3)")
    
    # Original evaluator
    result_orig = scheme_eval(expr, env)
    print(f"Original result: {result_orig}")
    
    # CPS evaluator
    result_cps = scheme_eval_cps(expr, env)
    print(f"CPS result: {result_cps}")
    
    # CPS optimized evaluator
    result_cps_opt = scheme_eval_cps_optimized(expr, env)
    print(f"CPS optimized result: {result_cps_opt}")
    
    assert result_orig == result_cps == result_cps_opt == 6
    print("✓ Basic arithmetic test passed!")

def test_nested_expression():
    """Test nested expressions"""
    env = create_global_frame()
    
    # Test expression: (+ (* 2 3) (- 10 5))
    expr = read_line("(+ (* 2 3) (- 10 5))")
    
    print("\nTesting: (+ (* 2 3) (- 10 5))")
    
    # Original evaluator
    result_orig = scheme_eval(expr, env)
    print(f"Original result: {result_orig}")
    
    # CPS evaluator
    result_cps = scheme_eval_cps(expr, env)
    print(f"CPS result: {result_cps}")
    
    # CPS optimized evaluator
    result_cps_opt = scheme_eval_cps_optimized(expr, env)
    print(f"CPS optimized result: {result_cps_opt}")
    
    assert result_orig == result_cps == result_cps_opt == 11
    print("✓ Nested expression test passed!")

def test_lambda_function():
    """Test lambda function evaluation"""
    env = create_global_frame()
    
    # Test expression: ((lambda (x) (+ x 1)) 5)
    expr = read_line("((lambda (x) (+ x 1)) 5)")
    
    print("\nTesting: ((lambda (x) (+ x 1)) 5)")
    
    try:
        # Original evaluator
        result_orig = scheme_eval(expr, env)
        print(f"Original result: {result_orig}")
        
        # CPS evaluator
        result_cps = scheme_eval_cps(expr, env)
        print(f"CPS result: {result_cps}")
        
        # CPS optimized evaluator
        result_cps_opt = scheme_eval_cps_optimized(expr, env)
        print(f"CPS optimized result: {result_cps_opt}")
        
        assert result_orig == result_cps == result_cps_opt == 6
        print("✓ Lambda function test passed!")
    except Exception as e:
        print(f"Lambda test failed: {e}")

if __name__ == "__main__":
    print("Testing CPS Implementation...")
    test_basic_arithmetic()
    test_nested_expression()
    test_lambda_function()
    print("\nAll tests completed!")
