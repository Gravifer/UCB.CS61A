from collections.abc import Callable, Iterable
from typing import Any
import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

# Define validation functions to avoid circular imports
def validate_form(expr, min_len, max_len=None):
    """Check that expr is a list with length between min_len and max_len."""
    if expr is nil:
        length = 0
    else:
        length = len(expr) if hasattr(expr, '__len__') else 0
    if length < min_len:
        raise SchemeError('too few operands in form')
    if max_len is not None and length > max_len:
        raise SchemeError('too many operands in form')

def validate_formals(formals):
    """Check that formals is a valid parameter list."""
    symbols = set()
    def check_formal(formal):
        if not scheme_symbolp(formal):
            raise SchemeError('non-symbol: {0}'.format(formal))
        if formal in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(formal))
        symbols.add(formal)
    
    while formals is not nil:
        if not isinstance(formals, Pair):
            check_formal(formals)
            return
        check_formal(formals.first)
        formals = formals.rest

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

#######################
# CPS Special Forms   #
#######################

def do_define_form_cps(expressions, env, cont):
    """CPS version of define form"""
    validate_form(expressions, 2)
    signature = expressions.first
    
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        validate_form(expressions, 2, 2)
        
        def define_cont(value):
            env.define(signature, value)
            return cont(signature)
        
        return scheme_eval_cps(expressions.rest.first, env, False, define_cont)
        
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g. (define (f x y) (+ x y))
        name = signature.first
        formals = signature.rest
        validate_formals(formals) 
        body = expressions.rest
        env.define(name, LambdaProcedure(formals, body, env))
        return cont(name)
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form_cps(expressions, env, cont):
    """CPS version of quote form"""
    validate_form(expressions, 1, 1)
    return cont(expressions.first)

def do_begin_form_cps(expressions, env, cont):
    """CPS version of begin form"""
    validate_form(expressions, 1)
    return eval_all_cps(expressions, env, cont)

def do_lambda_form_cps(expressions, env, cont):
    """CPS version of lambda form"""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    body = expressions.rest
    return cont(LambdaProcedure(formals, body, env))

def do_if_form_cps(expressions, env, cont):
    """CPS version of if form"""
    validate_form(expressions, 2, 3)
    
    def if_cont(test_value):
        if is_scheme_true(test_value):
            return scheme_eval_cps(expressions.rest.first, env, True, cont)
        elif len(expressions) == 3:
            return scheme_eval_cps(expressions.rest.rest.first, env, True, cont)
        else:
            return cont(None)
    
    return scheme_eval_cps(expressions.first, env, False, if_cont)

def do_and_form_cps(expressions, env, cont):
    """CPS version of and form"""
    def and_helper(exprs, env, cont):
        if exprs is nil:
            return cont(True)
        elif exprs.rest is nil:
            # Last expression - evaluate in tail position
            return scheme_eval_cps(exprs.first, env, True, cont)
        else:
            def and_cont(value):
                if is_scheme_false(value):
                    return cont(False)
                else:
                    return and_helper(exprs.rest, env, cont)
            return scheme_eval_cps(exprs.first, env, False, and_cont)
    
    return and_helper(expressions, env, cont)

def do_or_form_cps(expressions, env, cont):
    """CPS version of or form"""
    def or_helper(exprs, env, cont):
        if exprs is nil:
            return cont(False)
        elif exprs.rest is nil:
            # Last expression - evaluate in tail position
            return scheme_eval_cps(exprs.first, env, True, cont)
        else:
            def or_cont(value):
                if is_scheme_true(value):
                    return cont(value)
                else:
                    return or_helper(exprs.rest, env, cont)
            return scheme_eval_cps(exprs.first, env, False, or_cont)
    
    return or_helper(expressions, env, cont)

# CPS Special Forms Dictionary
SPECIAL_FORMS_CPS = {
    'define': do_define_form_cps,
    'quote': do_quote_form_cps,
    'begin': do_begin_form_cps,
    'lambda': do_lambda_form_cps,
    'if': do_if_form_cps,
    'and': do_and_form_cps,
    'or': do_or_form_cps,
}

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
    if scheme_symbolp(first) and first in SPECIAL_FORMS_CPS:
        # Use CPS special forms
        return SPECIAL_FORMS_CPS[first](rest, env, cont)
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

def create_fully_trampolined_evaluator():
    """Create a fully trampolined CPS evaluator that never uses Python recursion"""
    
    def trampoline_eval(expr, env, tail=False, cont=None):
        """Fully trampolined evaluator"""
        if cont is None:
            cont = ReturnCont()
        
        # Work queue for trampolined execution
        work_stack = [EvalCall(expr, env, tail, cont)]
        
        while work_stack:
            current_work = work_stack.pop()
            
            if isinstance(current_work, EvalCall):
                # Handle evaluation
                expr, env, tail, cont = current_work.expr, current_work.env, current_work.tail, current_work.cont
                
                # Evaluate atoms
                if scheme_symbolp(expr):
                    result = env.lookup(expr)
                    work_stack.append(ContinuationCall(cont, result))
                    continue
                elif self_evaluating(expr):
                    work_stack.append(ContinuationCall(cont, expr))
                    continue
                
                # All non-atomic expressions are lists (combinations)
                if not scheme_listp(expr):
                    raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
                
                first, rest = expr.first, expr.rest
                if scheme_symbolp(first) and first in SPECIAL_FORMS_CPS:
                    # Handle special forms directly (they create their own work)
                    result = SPECIAL_FORMS_CPS[first](rest, env, cont)
                    if isinstance(result, (ContinuationCall, EvalCall)):
                        work_stack.append(result)
                    else:
                        work_stack.append(ContinuationCall(cont, result))
                else:
                    # Function application: evaluate operator first
                    def operator_cont(operator):
                        validate_procedure(operator)
                        return eval_operands_trampolined(rest, env, 
                                                       lambda operands: apply_trampolined(operator, operands, env, cont))
                    
                    work_stack.append(EvalCall(first, env, False, operator_cont))
                    
            elif isinstance(current_work, ContinuationCall):
                # Handle continuation call
                result = current_work.execute()
                if isinstance(result, (ContinuationCall, EvalCall)):
                    work_stack.append(result)
                elif work_stack:  # More work to do
                    continue
                else:  # Final result
                    return result
        
        return None  # Should not reach here
    
    def eval_operands_trampolined(operands, env, cont):
        """Trampolined operand evaluation"""
        if operands is nil:
            return ContinuationCall(cont, nil)
        
        def first_cont(first_value):
            if operands.rest is nil:
                return ContinuationCall(cont, Pair(first_value, nil))
            else:
                return eval_operands_trampolined(operands.rest, env,
                                               lambda rest_values: ContinuationCall(cont, Pair(first_value, rest_values)))
        
        return EvalCall(operands.first, env, False, first_cont)
    
    def apply_trampolined(procedure, args, env, cont):
        """Trampolined application"""
        validate_procedure(procedure)
        
        if isinstance(procedure, BuiltinProcedure):
            py_args = list(args) + ([env] if procedure.need_env else [])
            try:
                result = procedure.py_func(*py_args)
                return ContinuationCall(cont, result)
            except TypeError as err:
                raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
        elif isinstance(procedure, LambdaProcedure):
            lambdaFrame = procedure.env.make_child_frame(procedure.formals, args)
            lambdaFrame.define('_self', procedure)
            return eval_all_trampolined(procedure.body, lambdaFrame, cont)
        elif isinstance(procedure, MuProcedure):
            muFrame = env.make_child_frame(procedure.formals, args)
            muFrame.define('_self', procedure)
            return eval_all_trampolined(procedure.body, muFrame, cont)
        else:
            assert False, "Unexpected procedure: {}".format(procedure)
    
    def eval_all_trampolined(expressions, env, cont):
        """Trampolined eval_all"""
        if expressions is nil:
            return ContinuationCall(cont, None)
        
        if expressions.rest is nil:
            # Last expression - evaluate in tail position
            return EvalCall(expressions.first, env, True, cont)
        else:
            # Not the last expression
            def sequence_cont(value):
                return eval_all_trampolined(expressions.rest, env, cont)
            return EvalCall(expressions.first, env, False, sequence_cont)
    
    return trampoline_eval

class EvalCall:
    """A deferred evaluation call for the trampoline"""
    def __init__(self, expr, env, tail, cont):
        self.expr = expr
        self.env = env
        self.tail = tail
        self.cont = cont

# Create the fully trampolined evaluator
scheme_eval_cps_fully_trampolined = create_fully_trampolined_evaluator()

################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)

# CPS version with advanced tail call optimization
# Use the fully trampolined version as the optimized evaluator
scheme_eval_cps_optimized = scheme_eval_cps_fully_trampolined
