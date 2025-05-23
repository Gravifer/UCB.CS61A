import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
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
        operator = scheme_eval(first, env)
        validate_procedure(operator)
        operands = rest.map(lambda x : scheme_eval(x, env))
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
        # * basic version:
        # py_args = []
        # while args is not nil:
        #     py_args.append(args.first)
        #     args = args.rest
        # if procedure.need_env:
        #     py_args.append(env)

        # ! monkey patching version:
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
        py_args = list(args) + ([env] if procedure.need_env else [])
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
        # ! monkey patching version:
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
        lambdaFrame = procedure.env.make_child_frame(procedure.formals, args)
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
        # ! monkey patching version:
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
        muFrame = env.make_child_frame(procedure.formals, args)
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
        scheme_eval(exprs.first, env)
        exprs = exprs.rest
    return scheme_eval(exprs.first, env, True)
    # END PROBLEM 6


################################
# Extra Credit: Tail Recursion #
################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
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
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
