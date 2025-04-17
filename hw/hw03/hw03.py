HW_SOURCE_FILE = __file__


def num_eights(n):
    """Returns the number of times 8 appears as a digit of n.

    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    >>> num_eights(8782089)
    3
    >>> from construct_check import check
    >>> # ban all assignment statements
    >>> check(HW_SOURCE_FILE, 'num_eights',
    ...       ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n == 0:
        return 0
    elif n % 10 == 8:
        return 1 + num_eights(n // 10)
    else:
        return num_eights(n // 10)


def digit_distance(n):
    """Determines the digit distance of n.

    >>> digit_distance(3)
    0
    >>> digit_distance(777) # 0 + 0
    0
    >>> digit_distance(314) # 2 + 3
    5
    >>> digit_distance(31415926535) # 2 + 3 + 3 + 4 + ... + 2
    32
    >>> digit_distance(3464660003)  # 1 + 2 + 2 + 2 + ... + 3
    16
    >>> from construct_check import check
    >>> # ban all loops
    >>> check(HW_SOURCE_FILE, 'digit_distance',
    ...       ['For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n < 10:
        return 0
    else:
        last_digit = n % 10
        second_last_digit = (n // 10) % 10
        return abs(last_digit - second_last_digit) + digit_distance(n // 10)


def interleaved_sum(n, odd_func, even_func):
    """Compute the sum odd_func(1) + even_func(2) + odd_func(3) + ..., up
    to n.

    >>> identity = lambda x: x
    >>> square = lambda x: x * x
    >>> triple = lambda x: x * 3
    >>> interleaved_sum(5, identity, square) # 1   + 2*2 + 3   + 4*4 + 5
    29
    >>> interleaved_sum(5, square, identity) # 1*1 + 2   + 3*3 + 4   + 5*5
    41
    >>> interleaved_sum(4, triple, square)   # 1*3 + 2*2 + 3*3 + 4*4
    32
    >>> interleaved_sum(4, square, triple)   # 1*1 + 2*3 + 3*3 + 4*3
    28
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'interleaved_sum', ['While', 'For', 'Mod']) # ban loops and %
    True
    >>> check(HW_SOURCE_FILE, 'interleaved_sum', ['BitAnd', 'BitOr', 'BitXor']) # ban bitwise operators, don't worry about these if you don't know what they are
    True
    """
    "*** YOUR CODE HERE ***"
    def odd_sum(k, n, odd_func, even_func): # assert k is odd
        # assert k % 2 == 1
        if k == n:
            return odd_func(k)
        elif k > n:
            return 0
        else:
            return odd_func(k) + even_func(k + 1) + odd_sum(k + 2, n, odd_func, even_func)
    return odd_sum(1, n, odd_func, even_func)


def next_smaller_dollar(bill):
    """Returns the next smaller bill in order."""
    if bill == 100:
        return 50
    if bill == 50:
        return 20
    if bill == 20:
        return 10
    elif bill == 10:
        return 5
    elif bill == 5:
        return 1

def count_dollars(total):
    """Return the number of ways to make change.

    >>> count_dollars(15)  # 15 $1 bills, 10 $1 & 1 $5 bills, ... 1 $5 & 1 $10 bills
    6
    >>> count_dollars(10)  # 10 $1 bills, 5 $1 & 1 $5 bills, 2 $5 bills, 10 $1 bills
    4
    >>> count_dollars(20)  # 20 $1 bills, 15 $1 & $5 bills, ... 1 $20 bill
    10
    >>> count_dollars(45)  # How many ways to make change for 45 dollars?
    44
    >>> count_dollars(100) # How many ways to make change for 100 dollars?
    344
    >>> count_dollars(200) # How many ways to make change for 200 dollars?
    3274
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_dollars', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    def count_dollars_helper(total, bill):
        """Return the number of ways to make change for total using bills <= bill."""
        if total == 0:
            return 1
        elif total < 0 or not bill:
            return 0
        elif bill == 1:
            return 1
        else:
            return (count_dollars_helper(total - bill, bill) 
                    + count_dollars_helper(total, next_smaller_dollar(bill)))
    return count_dollars_helper(total, 100)


def next_larger_dollar(bill):
    """Returns the next larger bill in order."""
    if bill == 1:
        return 5
    elif bill == 5:
        return 10
    elif bill == 10:
        return 20
    elif bill == 20:
        return 50
    elif bill == 50:
        return 100

def count_dollars_upward(total):
    """Return the number of ways to make change using bills.

    >>> count_dollars_upward(15)  # 15 $1 bills, 10 $1 & 1 $5 bills, ... 1 $5 & 1 $10 bills
    6
    >>> count_dollars_upward(10)  # 10 $1 bills, 5 $1 & 1 $5 bills, 2 $5 bills, 10 $1 bills
    4
    >>> count_dollars_upward(20)  # 20 $1 bills, 15 $1 & $5 bills, ... 1 $20 bill
    10
    >>> count_dollars_upward(45)  # How many ways to make change for 45 dollars?
    44
    >>> count_dollars_upward(100) # How many ways to make change for 100 dollars?
    344
    >>> count_dollars_upward(200) # How many ways to make change for 200 dollars?
    3274
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_dollars_upward', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    def count_dollars_helper(total, bill):
        """Return the number of ways to make change for total using bills >= bill."""
        if total == 0:
            return 1
        elif total < 0 or not bill:
            return 0
        elif bill == 100:
            return count_dollars_helper(total - bill, bill)
        else:
            return (count_dollars_helper(total - bill, bill) 
                    + count_dollars_helper(total, next_larger_dollar(bill)))
    return count_dollars_helper(total, 1)


def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    "*** YOUR CODE HERE ***"
    if n == 1:
        print_move(start, end)
        return 
    mid = 6 - start - end
    move_stack(n - 1, start, mid)
    print_move(start, end)
    move_stack(n - 1, mid, end)


from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial',
    ...     ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'FunctionDef', 'Recursion'])
    True
    """
    # https://pythontutor.com/cp/composingprograms.html#code=def%20make_anonymous_factorial%28%29%3A%0A%20%20%20%20%22%22%22Return%20the%20value%20of%20an%20expression%20that%20computes%20factorial.%0A%0A%20%20%20%20%3E%3E%3E%20make_anonymous_factorial%28%29%285%29%0A%20%20%20%20120%0A%20%20%20%20%3E%3E%3E%20from%20construct_check%20import%20check%0A%20%20%20%20%3E%3E%3E%20%23%20ban%20any%20assignments%20or%20recursion%0A%20%20%20%20%3E%3E%3E%20check%28HW_SOURCE_FILE,%20'make_anonymous_factorial',%0A%20%20%20%20...%20%20%20%20%20%5B'Assign',%20'AnnAssign',%20'AugAssign',%20'NamedExpr',%20'FunctionDef',%20'Recursion'%5D%29%0A%20%20%20%20True%0A%20%20%20%20%22%22%22%0A%20%20%20%20%23%20just%20need%20a%20Y-combinator%3A%20%CE%BBf.%28%CE%BBx.f%28x%20x%29%29%28%CE%BBx.f%28x%20x%29%29%0A%20%20%20%20%23%20in%20R%3A%20%22%28%5C%28f%29%20%28%5C%28x%29%20f%28x%28x%29%29%29%28%5C%28x%29%20f%28x%28x%29%29%29%29%20%28%5C%28f%29%20%5C%28n%29%20if%20%28n%20%3D%3D%200%29%201%20else%20n%20*%20f%28n%20-%201%29%29%20%285%29%22%0A%20%20%20%20def%20Y%28f%29%3A%20%0A%20%20%20%20%20%20%20%20%22%22%22Actually%20a%20Z-combinator%22%22%22%0A%20%20%20%20%20%20%20%20state%20%3D%20f.__str__%28%29%0A%20%20%20%20%20%20%20%20def%20F%28g%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20state%20%3D%20g.__str__%28%29%0A%20%20%20%20%20%20%20%20%20%20%20%20def%20G%28x%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20state%20%3D%20x.__str__%28%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20def%20h%28y%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20state%20%3D%20y.__str__%28%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20X%20%3D%20x%28x%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20xxy%20%3D%20X%28y%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20xxy%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20h.__str__%20%3D%20%28lambda%20%3A%20%22h%28%22%2Bstate%2B%22%29%22%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20g%28h%29%0A%20%20%20%20%20%20%20%20%20%20%20%20G.__str__%20%3D%20%28lambda%20%3A%20%22G%28%22%2Bstate%2B%22%29%22%29%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20G%0A%20%20%20%20%20%20%20%20F.__str__%20%3D%20%28lambda%20%3A%20%22F%28%22%2Bstate%2B%22%29%22%29%0A%20%20%20%20%20%20%20%20return%20F%28f%29%28F%28f%29%29%0A%20%20%20%20mk_fib%20%3D%20%28lambda%20fib%3A%20lambda%20n%3A%201%20if%20n%20%3D%3D%200%20else%20n%20*%20fib%28n%20-%201%29%29%20%23%20factorial%20function%0A%20%20%20%20mk_fib.__str__%20%3D%20%28lambda%20%3A%20%22mk_fib%22%29%0A%20%20%20%20return%20Y%28mk_fib%29%0Aanonymous_factorial%20%3D%20make_anonymous_factorial%28%29%0Ares%20%3D%20anonymous_factorial%281%29%20%23%20any%20more%20will%20not%20be%20eligible&cumulative=false&mode=edit&origin=composingprograms.js&py=3&rawInputLstJSON=%5B%5D
    # just need a Y-combinator: λf.(λx.f(x x))(λx.f(x x))
    # in R: "(\(f) (\(x) f(x(x)))(\(x) f(x(x)))) (\(f) \(n) if (n == 0) 1 else n * f(n - 1)) (5)"
    return (lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))( # Z-combinator 
        lambda f: lambda n: 1 if n == 0 else n * f(n - 1)) # factorial function

