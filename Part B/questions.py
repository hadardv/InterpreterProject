from functools import reduce
from functools import reduce

## question 1
fib = lambda n: [0, 1] if n <= 2 else [0, 1] + [fib(n - 1)[-1] + fib(n - 1)[-2] for i in range(2, n)]

## question 2
concat = lambda l: l[0] if len(l) == 1 else l[0] + ' ' + concat(l[1:])

## question 3
cumulative_sum_squares = lambda lists: (lambda f: f(f, lists, []))(
    lambda self, lst, result: result if not lst else self(
        self, lst[1:], result + [(lambda l: sum(
            (lambda x: x * x)(n) for n in l if n % 2 == 0
        ))(lst[0])]
    )
)


## question 4
def cumulative_op(op):
    return lambda seq: (lambda f: f(f, seq, seq[0]))(
        lambda self, s, result: result if len(s) == 1 else self(s[1:], op(result, s[1]))
    )


# Factorial function
factorial = lambda n: cumulative_op(lambda x, y: x * y)([1] + list(range(1, n + 1)))

# Exponentiation function
exponentiation = lambda base, exp: cumulative_op(lambda x, y: x * base)([1] * exp)

# Examples of usage
print(factorial(5))  # Calculates 5!
print(exponentiation(2, 3))  #Calculates 2^3

## question 5
print(reduce(lambda x, y: x + y, map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]))))

## question 6
palindrome_counter = lambda list_of_lists: list(
    map(lambda sublist: reduce(lambda count, s: count + (s.lower() == s.lower()[::-1]),
                               filter(lambda s: isinstance(s, str), sublist), 0), list_of_lists))

## question 7
# Lazy evaluation delays computation until results are needed.
# In the program, the lazy approach uses a generator (generate_values())
# and doesn't compute squared values until print(squared_values) is called,
# contrasting with eager evaluation which computes all values upfront.

## question 8
prime_filter_sort = lambda nums: sorted(
    [n for n in nums if n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))], reverse=True)

