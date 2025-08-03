from collections.abc import Callable, Iterable
from typing import Any
import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

# ! monkey patching Pair and nil
if not hasattr(Pair, "__iter__"): # patch only once; should __iter__ be natively defined, monkey-patch doesn't occur
    def _pair_iter__(obj):
        """Convert the Pair object to an iterable for use with list()."""
        current = obj
        while isinstance(current, Pair):
            yield current.first
            current = current.rest
        if current is nil:
            return
        # If `rest` is not `nil`, we should raise an error for improper list
        if current is not nil:
            raise TypeError('ill-formed list (not properly terminated with nil)')
    Pair.__iter__ = _pair_iter__
    nil.__class__.__iter__ = lambda self: iter([])  # Make nil iterable

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored; used for tail recursion optimization
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        operator = scheme_eval(first, env, False)
        validate_procedure(operator)
        operands = rest.map(lambda x : scheme_eval(x, env, False)) #! map is already defined in Pair as provided
        return scheme_apply(operator, operands, env)
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        py_args = list(args) + ([env] if procedure.need_env else []) #! require monkey patched Pair
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            return procedure.py_func(*py_args)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        lambdaFrame = procedure.env.make_child_frame(procedure.formals, args) #! require monkey patched Pair
        lambdaFrame.define('_self', procedure)
        # // print("DEBUG: lambdaFrame created: ", lambdaFrame)
        # the created frame remains a child to the defining frame; 
        # this is called lexical scoping. 
        # It is still possible to transfer it to the calling scope, 
        # with bindings of its former ancestors added,
        # but this optimization is not intended here.
        # the other possibility is to inherit the calling scope (which would be wrong for this assignment)
        try:
            return eval_all(procedure.body, lambdaFrame)
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure): # ! Mu means something else in the literature!
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        muFrame = env.make_child_frame(procedure.formals, args) #! require monkey patched Pair
        muFrame.define('_self', procedure)
        # this is called dynamic scoping
        try:
            return eval_all(procedure.body, muFrame)
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    #// return scheme_eval(expressions.first, env) # replace this with lines of your own code
    if expressions is nil:
        return None
    exprs = expressions
    while exprs.rest is not nil:
        scheme_eval(exprs.first, env, False)
        exprs = exprs.rest
    return scheme_eval(exprs.first, env, True)
    # END PROBLEM 6


######################
# CPS Implementation #
######################

class ReturnCont:
    """Final continuation - just returns the value"""
    def __call__(self, value):
        return value

class ApplyCont:
    """Continuation for applying a procedure after evaluating operator"""
    def __init__(self, operands_expr, env, cont):
        self.operands_expr = operands_expr
        self.env = env
        self.cont = cont
    
    def __call__(self, operator):
        # Evaluate operands, then apply
        validate_procedure(operator)
        return eval_operands_cps(self.operands_expr, self.env, 
                               ApplyProcCont(operator, self.env, self.cont))

class ApplyProcCont:
    """Continuation for actually applying the procedure"""
    def __init__(self, operator, env, cont):
        self.operator = operator
        self.env = env
        self.cont = cont
    
    def __call__(self, operands):
        return scheme_apply_cps(self.operator, operands, self.env, self.cont)

class EvalSequenceCont:
    """Continuation for evaluating remaining expressions in a sequence"""
    def __init__(self, remaining_exprs, env, cont):
        self.remaining_exprs = remaining_exprs
        self.env = env
        self.cont = cont
    
    def __call__(self, value):
        # Ignore the value and continue with remaining expressions
        return eval_all_cps(self.remaining_exprs, self.env, self.cont)

def eval_operands_cps(operands, env, cont):
    """CPS version: Evaluate a list of operands and pass the result list to continuation"""
    if operands is nil:
        return cont(nil)
    
    class OperandCont:
        def __init__(self, remaining, env, cont):
            self.remaining = remaining
            self.env = env
            self.cont = cont
        
        def __call__(self, first_value):
            if self.remaining is nil:
                return self.cont(Pair(first_value, nil))
            else:
                return eval_operands_cps(self.remaining, self.env, 
                                       lambda rest_values: self.cont(Pair(first_value, rest_values)))
    
    return scheme_eval_cps(operands.first, env, False, 
                          OperandCont(operands.rest, env, cont))

def scheme_eval_cps(expr, env, tail=False, cont=None):
    """CPS version of scheme_eval with proper tail call optimization"""
    if cont is None:
        cont = ReturnCont()
    
    # Evaluate atoms
    if scheme_symbolp(expr):
        return cont(env.lookup(expr))
    elif self_evaluating(expr):
        return cont(expr)

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        # For now, fall back to original special forms
        # TODO: Convert special forms to CPS
        try:
            result = scheme_forms.SPECIAL_FORMS[first](rest, env)
            return cont(result)
        except Exception as e:
            raise e
    else:
        # CPS version: evaluate operator, then operands, then apply
        return scheme_eval_cps(first, env, False, ApplyCont(rest, env, cont))

def scheme_apply_cps(procedure, args, env, cont=None):
    """CPS version of scheme_apply"""
    if cont is None:
        cont = ReturnCont()
        
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        py_args = list(args) + ([env] if procedure.need_env else [])
        try:
            result = procedure.py_func(*py_args)
            return cont(result)
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        lambdaFrame = procedure.env.make_child_frame(procedure.formals, args)
        lambdaFrame.define('_self', procedure)
        try:
            return eval_all_cps(procedure.body, lambdaFrame, cont)
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, MuProcedure):
        muFrame = env.make_child_frame(procedure.formals, args)
        muFrame.define('_self', procedure)
        try:
            return eval_all_cps(procedure.body, muFrame, cont)
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all_cps(expressions, env, cont=None):
    """CPS version of eval_all"""
    if cont is None:
        cont = ReturnCont()
        
    if expressions is nil:
        return cont(None)
    
    if expressions.rest is nil:
        # Last expression - evaluate in tail position
        return scheme_eval_cps(expressions.first, env, True, cont)
    else:
        # Not the last expression - evaluate and continue with the rest
        return scheme_eval_cps(expressions.first, env, False, 
                              EvalSequenceCont(expressions.rest, env, cont))


################################
# Extra Credit: Tail Recursion #
################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

class ContinuationCall:
    """A continuation call that should be trampolined"""
    def __init__(self, cont, value):
        self.cont = cont
        self.value = value
    
    def execute(self):
        return self.cont(self.value)

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval: Callable[..., Any]):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        while isinstance(result, Unevaluated):
            result = unoptimized_scheme_eval(result.expr, result.env)
        return result
        # END OPTIONAL PROBLEM 1
    return optimized_eval

def optimize_tail_calls_cps(scheme_eval_cps_func: Callable[..., Any]):
    """Return a CPS-compatible tail recursive version of scheme_eval_cps."""
    def optimized_eval_cps(expr, env, tail=False, cont=None):
        """CPS Evaluate Scheme expression EXPR in Frame ENV with continuation CONT."""
        if cont is None:
            cont = ReturnCont()
            
        # For CPS, we use a trampoline for continuation calls
        class TrampolineCont:
            def __init__(self, original_cont, is_tail):
                self.original_cont = original_cont
                self.is_tail = is_tail
            
            def __call__(self, value):
                if self.is_tail:
                    return ContinuationCall(self.original_cont, value)
                else:
                    return self.original_cont(value)
        
        result = scheme_eval_cps_func(expr, env, tail, TrampolineCont(cont, tail))
        
        # Trampoline loop for continuation calls
        while isinstance(result, ContinuationCall):
            result = result.execute()
            
        return result
    return optimized_eval_cps

################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)

# CPS version with advanced tail call optimization
scheme_eval_cps_optimized = optimize_tail_calls_cps(scheme_eval_cps)
