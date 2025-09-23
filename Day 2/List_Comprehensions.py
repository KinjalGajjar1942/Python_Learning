# Squares of numbers
squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

# Conditional
evens = [x for x in range(10) if x % 2 == 0]
print(evens)    # [0, 2, 4, 6, 8]

# Nested
pairs = [(x,y) for x in [1,2] for y in [3,4]]
print(pairs)    # [(1,3),(1,4),(2,3),(2,4)]



# Lambda functions

# Normal function
def square(x):
    return x**2

# Lambda equivalent
square = lambda x: x**2
print(square(5))  # 25

# Lambda with multiple arguments
add = lambda a,b: a+b
print(add(3,4))  # 7

# Use in map/filter
nums = [1,2,3,4,5]
squares = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x%2==0, nums))
print(squares)  # [1,4,9,16,25]
print(evens)    # [2,4]
