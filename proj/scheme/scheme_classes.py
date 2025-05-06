import builtins
from math import e

from pair import *

class SchemeError(Exception):
    """Exception indicating an error in a Scheme program."""

################
# Environments #
################

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        self.bindings[symbol] = value
        #// return self # attempt to provide a fluent interface # q 01 doesn't like this; whatever
        # If the symbol is already defined in the current frame, 
        # it will be overwritten. This is the expected behavior in Scheme.
        # END PROBLEM 1

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        env = self
        while env is not None:
            if symbol in env.bindings:
                return env.bindings[symbol]
            env = env.parent
        # If we reach here, the symbol was not found in any frame.
        # END PROBLEM 1
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Both FORMALS and VALS are represented
        as Pairs. Raise an error if too many or too few vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        if len(formals) != len(vals):
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 8
        "*** YOUR CODE HERE ***"
        child_frame = Frame(self)

        # basic version
        # while formals is not nil:
        #     if isinstance(formals.first, str):
        #         child_frame.define(formals.first, vals.first)
        #     else:
        #         raise SchemeError('Invalid formal parameter: {0}'.format(formals.first))
        #     formals = formals.rest
        #     vals = vals.rest
    
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
        [child_frame.define(formal, val) for formal, val in zip(formals, vals)]

        return child_frame
        # END PROBLEM 8

##############
# Procedures #
##############

class Procedure:
    """The the base class for all Procedure classes."""

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, py_func, need_env=False, name='builtin'):
        self.name = name
        self.py_func = py_func
        self.need_env = need_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))
