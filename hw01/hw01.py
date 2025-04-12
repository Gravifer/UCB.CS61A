from operator import add, sub

def a_plus_abs_b(a, b):
    """Return a+abs(b), but without calling abs.

    >>> a_plus_abs_b(2, 3)
    5
    >>> a_plus_abs_b(2, -3)
    5
    >>> a_plus_abs_b(-1, 4)
    3
    >>> a_plus_abs_b(-1, -4)
    3
    """
    if b < 0:
        f = sub
    else:
        f = add
    return f(a, b)

def a_plus_abs_b_syntax_check():
    """Check that you didn't change the return statement of a_plus_abs_b.

    >>> # You aren't expected to understand the code of this test.
    >>> import inspect, re
    >>> re.findall(r'^\s*(return .*)', inspect.getsource(a_plus_abs_b), re.M)
    ['return f(a, b)']
    """
    # You don't need to edit this function. It's just here to check your work.


def two_of_three(i, j, k):
    """Return m*m + n*n, where m and n are the two smallest members of the
    positive numbers i, j, and k.

    >>> two_of_three(1, 2, 3)
    5
    >>> two_of_three(5, 3, 1)
    10
    >>> two_of_three(10, 2, 8)
    68
    >>> two_of_three(5, 5, 5)
    50
    """
    return add(i*i, add(j*j, k*k) - max(i, j, k)*max(i, j, k))

def two_of_three_syntax_check():
    """Check that your two_of_three code consists of nothing but a return statement.

    >>> # You aren't expected to understand the code of this test.
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(two_of_three)).body[0].body]
    ['Expr', 'Return']
    """
    # You don't need to edit this function. It's just here to check your work.


def largest_factor(n):
    """Return the largest factor of n that is smaller than n.

    >>> largest_factor(15) # factors are 1, 3, 5
    5
    >>> largest_factor(80) # factors are 1, 2, 4, 5, 8, 10, 16, 20, 40
    40
    >>> largest_factor(13) # factor is 1 since 13 is prime
    1
    """
    # # hard code largest true divisors for n less than 100
    # hard_coding = [1, 1, 1, 1, 2, 1, 3, 1, 4, 3, 
    #                5, 1, 4, 1, 7, 5, 8, 1, 9, 1, 
    #                10, 7, 11, 1, 12, 5, 13, 9, 14, 1,
    #                15, 1, 16, 1, 17, 1, 18, 9, 19, 1,
    #                20, 1, 21, 1, 22, 11, 23, 1, 24, 1,
    #                25, 1, 26, 13, 27, 1, 28, 1, 29, 1,
    #                30, 1, 31, 1, 32, 1, 33, 1, 34, 17,
    #                35, 1, 36, 1, 37, 1, 38, 19, 39, 1,
    #                40, 1, 41, 1, 42, 21, 43, 1, 44, 1,
    #                45, 1, 46, 23, 47, 1, 48, 1, 49, 1,
    #                50, 1, 51, 1, 52, 26, 53, 1, 54, 27]

    # Find the largest factor of n that is smaller than n
    # only check up to sqrt(n) to reduce time complexity
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return n // i
    for i in range(n-1, 1, -1):
        if n % i == 0:
            return i
    # If no factors are found, return 1
    return 1


def hailstone(n):
    """Print the hailstone sequence starting at n and return its
    length.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    >>> b = hailstone(1)
    1
    >>> b
    1
    """
    # 3n+1 conjecture
    length = 0
    while n != 1:
        print(n)
        length += 1
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
    print(n)
    return length + 1


