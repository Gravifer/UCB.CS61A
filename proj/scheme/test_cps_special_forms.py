#!/usr/bin/env python3

"""Test CPS with pre-defined functions to avoid circular imports"""

import sys
import os

sys.path.append("scheme_reader")

from scheme_eval_apply import scheme_eval_cps, scheme_eval_cps_optimized
from scheme_reader import read_line
from scheme_classes import *
from scheme import create_global_frame

def test_cps_define():
    """Test CPS with define form"""
    env = create_global_frame()
    
    # Test simple define
    define_expr = read_line("(x 5)")
    print("Testing CPS define: (define x 5)")
    
    result = scheme_eval_cps(Pair('define', define_expr), env)
    print(f"Define result: {result}")
    
    # Test lookup
    lookup_expr = read_line("x")
    result = scheme_eval_cps(lookup_expr, env)
    print(f"Lookup result: {result}")
    
    assert result == 5
    print("✓ CPS define test passed!")

def test_cps_if():
    """Test CPS with if form"""
    env = create_global_frame()
    
    # Test if true
    if_expr = read_line("(#t 42 99)")
    print("\nTesting CPS if: (if #t 42 99)")
    
    result = scheme_eval_cps(Pair('if', if_expr), env)
    print(f"If result: {result}")
    
    assert result == 42
    
    # Test if false
    if_expr2 = read_line("(#f 42 99)")
    print("Testing CPS if: (if #f 42 99)")
    
    result2 = scheme_eval_cps(Pair('if', if_expr2), env)
    print(f"If result: {result2}")
    
    assert result2 == 99
    print("✓ CPS if test passed!")

def test_cps_lambda():
    """Test CPS with lambda form"""
    env = create_global_frame()
    
    # Create lambda
    lambda_expr = read_line("((x) (+ x 1))")
    print("\nTesting CPS lambda: (lambda (x) (+ x 1))")
    
    lambda_proc = scheme_eval_cps(Pair('lambda', lambda_expr), env)
    print(f"Lambda result: {lambda_proc}")
    
    assert isinstance(lambda_proc, LambdaProcedure)
    print("✓ CPS lambda test passed!")

def test_cps_arithmetic():
    """Test CPS with arithmetic"""
    env = create_global_frame()
    
    # Test nested arithmetic
    arith_expr = read_line("(+ (* 3 4) (- 10 5))")
    print("\nTesting CPS arithmetic: (+ (* 3 4) (- 10 5))")
    
    result = scheme_eval_cps(arith_expr, env)
    print(f"Result: {result}")
    
    result_opt = scheme_eval_cps_optimized(arith_expr, env)
    print(f"Optimized result: {result_opt}")
    
    assert result == result_opt == 17
    print("✓ CPS arithmetic test passed!")

if __name__ == "__main__":
    print("Testing CPS Special Forms...")
    test_cps_define()
    test_cps_if()
    test_cps_lambda()
    test_cps_arithmetic()
    print("\nCPS special forms tests completed!")
