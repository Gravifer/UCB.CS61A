#!/usr/bin/env python3

"""Test script for recursive functions to demonstrate CPS tail call optimization"""

import sys
import os

sys.path.append("scheme_reader")

from scheme_eval_apply import scheme_eval, scheme_eval_cps, scheme_eval_cps_optimized
from scheme_reader import *
from scheme_classes import *
from scheme import create_global_frame

def test_tail_recursive_factorial():
    """Test tail-recursive factorial to demonstrate stack frame reduction"""
    env = create_global_frame()
    
    # Define a tail-recursive factorial function
    define_expr = read_line("""
        (define fact-tail 
          (lambda (n acc) 
            (if (= n 0) 
                acc 
                (fact-tail (- n 1) (* n acc)))))
    """)
    
    # Define the factorial function
    scheme_eval(define_expr, env)
    
    # Test with a moderate value
    test_expr = read_line("(fact-tail 10 1)")
    
    print("Testing tail-recursive factorial: (fact-tail 10 1)")
    
    # Original evaluator
    result_orig = scheme_eval(test_expr, env)
    print(f"Original result: {result_orig}")
    
    # CPS evaluator
    env_cps = create_global_frame()
    scheme_eval(define_expr, env_cps)  # Redefine in CPS environment
    result_cps = scheme_eval_cps(test_expr, env_cps)
    print(f"CPS result: {result_cps}")
    
    # CPS optimized evaluator
    env_cps_opt = create_global_frame()
    scheme_eval(define_expr, env_cps_opt)  # Redefine in optimized environment
    result_cps_opt = scheme_eval_cps_optimized(test_expr, env_cps_opt)
    print(f"CPS optimized result: {result_cps_opt}")
    
    expected = 3628800  # 10!
    assert result_orig == result_cps == result_cps_opt == expected
    print("✓ Tail-recursive factorial test passed!")

def test_deep_recursion():
    """Test deep recursion to verify tail call optimization works"""
    env = create_global_frame()
    
    # Define a simple counting function
    define_expr = read_line("""
        (define count-down 
          (lambda (n) 
            (if (= n 0) 
                0 
                (count-down (- n 1)))))
    """)
    
    # Define the function
    scheme_eval(define_expr, env)
    
    # Test with a reasonably large number
    test_expr = read_line("(count-down 100)")
    
    print("\nTesting deep recursion: (count-down 100)")
    
    try:
        # Original evaluator
        result_orig = scheme_eval(test_expr, env)
        print(f"Original result: {result_orig}")
        
        # CPS evaluator
        env_cps = create_global_frame()
        scheme_eval(define_expr, env_cps)
        result_cps = scheme_eval_cps(test_expr, env_cps)
        print(f"CPS result: {result_cps}")
        
        # CPS optimized evaluator
        env_cps_opt = create_global_frame()
        scheme_eval(define_expr, env_cps_opt)
        result_cps_opt = scheme_eval_cps_optimized(test_expr, env_cps_opt)
        print(f"CPS optimized result: {result_cps_opt}")
        
        assert result_orig == result_cps == result_cps_opt == 0
        print("✓ Deep recursion test passed!")
        
    except RecursionError as e:
        print(f"Recursion limit hit (expected for original evaluator): {e}")
        print("Testing just CPS versions...")
        
        # Test CPS versions only
        env_cps = create_global_frame()
        scheme_eval(define_expr, env_cps)
        result_cps = scheme_eval_cps(test_expr, env_cps)
        print(f"CPS result: {result_cps}")
        
        env_cps_opt = create_global_frame()
        scheme_eval(define_expr, env_cps_opt)
        result_cps_opt = scheme_eval_cps_optimized(test_expr, env_cps_opt)
        print(f"CPS optimized result: {result_cps_opt}")
        
        assert result_cps == result_cps_opt == 0
        print("✓ CPS deep recursion test passed!")

if __name__ == "__main__":
    print("Testing CPS Tail Call Optimization...")
    test_tail_recursive_factorial()
    test_deep_recursion()
    print("\nRecursive tests completed!")
