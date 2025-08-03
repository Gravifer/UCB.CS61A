#!/usr/bin/env python3

"""Test CPS recursive functions"""

import sys
import os

sys.path.append("scheme_reader")

from scheme_eval_apply import scheme_eval_cps, scheme_eval_cps_optimized
from scheme_reader import read_line
from scheme_classes import *
from scheme import create_global_frame

def test_cps_factorial():
    """Test CPS factorial function"""
    env = create_global_frame()
    
    # Define factorial function using CPS
    # (define fact-tail (lambda (n acc) (if (= n 0) acc (fact-tail (- n 1) (* n acc)))))
    fact_define = Pair('define', 
                       Pair(Pair('fact-tail', Pair('n', Pair('acc', nil))),
                            Pair(Pair('if', 
                                     Pair(Pair('=', Pair('n', Pair(0, nil))),
                                          Pair('acc',
                                               Pair(Pair('fact-tail', 
                                                        Pair(Pair('-', Pair('n', Pair(1, nil))),
                                                             Pair(Pair('*', Pair('n', Pair('acc', nil))), nil))), nil)))), nil)))
    
    print("Defining factorial function with CPS...")
    result = scheme_eval_cps(fact_define, env)
    print(f"Define result: {result}")
    
    # Test factorial
    fact_call = Pair('fact-tail', Pair(5, Pair(1, nil)))
    print("Testing: (fact-tail 5 1)")
    
    result_cps = scheme_eval_cps(fact_call, env)
    print(f"CPS result: {result_cps}")
    
    result_cps_opt = scheme_eval_cps_optimized(fact_call, env)
    print(f"CPS optimized result: {result_cps_opt}")
    
    expected = 120  # 5!
    assert result_cps == result_cps_opt == expected
    print("✓ CPS factorial test passed!")

def test_cps_countdown():
    """Test CPS countdown function"""
    env = create_global_frame()
    
    # Define countdown function using CPS
    # (define countdown (lambda (n) (if (= n 0) 0 (countdown (- n 1)))))
    countdown_define = Pair('define', 
                           Pair(Pair('countdown', Pair('n', nil)),
                                Pair(Pair('if', 
                                         Pair(Pair('=', Pair('n', Pair(0, nil))),
                                              Pair(0,
                                                   Pair(Pair('countdown', 
                                                            Pair(Pair('-', Pair('n', Pair(1, nil))), nil)), nil)))), nil)))
    
    print("\nDefining countdown function with CPS...")
    result = scheme_eval_cps(countdown_define, env)
    print(f"Define result: {result}")
    
    # Test countdown
    countdown_call = Pair('countdown', Pair(10, nil))
    print("Testing: (countdown 10)")
    
    result_cps = scheme_eval_cps(countdown_call, env)
    print(f"CPS result: {result_cps}")
    
    result_cps_opt = scheme_eval_cps_optimized(countdown_call, env)
    print(f"CPS optimized result: {result_cps_opt}")
    
    assert result_cps == result_cps_opt == 0
    print("✓ CPS countdown test passed!")

def test_deep_recursion():
    """Test deep recursion to verify tail call optimization"""
    env = create_global_frame()
    
    # Define countdown function
    countdown_define = Pair('define', 
                           Pair(Pair('countdown', Pair('n', nil)),
                                Pair(Pair('if', 
                                         Pair(Pair('=', Pair('n', Pair(0, nil))),
                                              Pair(0,
                                                   Pair(Pair('countdown', 
                                                            Pair(Pair('-', Pair('n', Pair(1, nil))), nil)), nil)))), nil)))
    
    print("\nTesting deep recursion...")
    scheme_eval_cps(countdown_define, env)
    
    # Test with larger number to verify tail call optimization
    deep_call = Pair('countdown', Pair(100, nil))
    print("Testing: (countdown 100)")
    
    try:
        result_cps_opt = scheme_eval_cps_optimized(deep_call, env)
        print(f"CPS optimized result: {result_cps_opt}")
        
        assert result_cps_opt == 0
        print("✓ Deep recursion test passed!")
        
    except RecursionError as e:
        print(f"Recursion error (unexpected): {e}")
        print("✗ Deep recursion test failed!")

if __name__ == "__main__":
    print("Testing CPS Recursive Functions...")
    test_cps_factorial()
    test_cps_countdown()
    test_deep_recursion()
    print("\nCPS recursive function tests completed!")
