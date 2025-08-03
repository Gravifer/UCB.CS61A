#!/usr/bin/env python3

"""Simple test for CPS without special forms"""

import sys
import os

sys.path.append("scheme_reader")

from scheme_eval_apply import scheme_eval_cps, scheme_eval_cps_optimized
from scheme_reader import read_line
from scheme_classes import *
from scheme import create_global_frame

def test_simple_cps():
    """Test CPS with simple expressions that don't require special forms"""
    env = create_global_frame()
    
    # Test basic arithmetic
    expr1 = read_line("(+ 1 2 3)")
    print("Testing: (+ 1 2 3)")
    
    result_cps = scheme_eval_cps(expr1, env)
    print(f"CPS result: {result_cps}")
    
    result_cps_opt = scheme_eval_cps_optimized(expr1, env)
    print(f"CPS optimized result: {result_cps_opt}")
    
    assert result_cps == result_cps_opt == 6
    print("✓ Simple CPS test passed!")
    
    # Test nested expressions
    expr2 = read_line("(+ (* 2 3) (- 10 5))")
    print("\nTesting: (+ (* 2 3) (- 10 5))")
    
    result_cps = scheme_eval_cps(expr2, env)
    print(f"CPS result: {result_cps}")
    
    result_cps_opt = scheme_eval_cps_optimized(expr2, env)
    print(f"CPS optimized result: {result_cps_opt}")
    
    assert result_cps == result_cps_opt == 11
    print("✓ Nested CPS test passed!")

if __name__ == "__main__":
    print("Testing CPS Implementation (simple expressions)...")
    test_simple_cps()
    print("\nSimple CPS tests completed!")
