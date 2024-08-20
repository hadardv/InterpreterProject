from functools import reduce


def main():
    # 1. Fibonacci sequence generator
    fib = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n - 2), [0, 1]) if n > 2 else [0] * n
    print("1. Fibonacci sequence (n=8):",fib(8))

    # 2. String concatenation
    concat = lambda l: l[0] if len(l) == 1 else l[0] + ' ' + concat(l[1:])
    print("2. String concatenation:", concat(["Hello", "world", "from", "Python"]))

    # 3. Cumulative sum of squares of even numbers
    cumulative_sum_squares = lambda lists: (lambda f: f(f, lists, []))(
        lambda self, lst, result: result if not lst else self(
            self, lst[1:], result + [(lambda l: sum(
                (lambda x: x * x)(n) for n in l if n % 2 == 0
            ))(lst[0])]
        )
    )
    print("3. Cumulative sum of squares of even numbers:",
          cumulative_sum_squares([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))

    # 4. Higher-order cumulative operation
    def cumulative_op(op):
        return lambda seq: reduce(op, seq)

    factorial = lambda n: cumulative_op(lambda x, y: x * y)(range(1, n + 1))
    exponentiation = lambda base, exp: cumulative_op(lambda x, y: x * base)([base] * exp)
    print("4a. Factorial of 5:", factorial(5))
    print("4b. 2^3:", exponentiation(2,3))

    # 5. One-line sum of squared even numbers
    one_line_sum = lambda nums: reduce(lambda x, y: x + y, map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, nums)))
    print("5. Sum of squared even numbers:", one_line_sum([1, 2, 3, 4, 5, 6]))

    # 6. Palindrome counter
    palindrome_counter = lambda list_of_lists: list(
        map(lambda sublist: reduce(lambda count, s: count + (s.lower() == s.lower()[::-1]),
                                   filter(lambda s: isinstance(s, str), sublist), 0), list_of_lists))
    print("6. Palindrome count:", palindrome_counter([["racecar", "hello", "deified", 123], ["python", "madam", "code"],
                                                      ["level", "algorithm", "A man a plan a canal Panama"]]))

    # 7. Lazy evaluation demonstration
    def generate_values():
        print('Generating values...')
        yield 1
        yield 2
        yield 3

    def square(x):
        print(f'Squaring {x}')
        return x * x

    print("7. Lazy vs Eager evaluation:")
    print('Eager evaluation:')
    values = list(generate_values())
    squared_values = [square(x) for x in values]
    print(squared_values)

    print('\nLazy evaluation:')
    squared_values = [square(x) for x in generate_values()]
    print(squared_values)

    # 8. Prime filter and sort
    prime_filter_sort = lambda nums: sorted(
        [n for n in nums if n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))], reverse=True)
    print("8. Prime numbers sorted in descending order:", prime_filter_sort([10, 3, 7, 1, 13, 20, 23, 15, 29, 31]))


if __name__ == "__main__":
    main()
