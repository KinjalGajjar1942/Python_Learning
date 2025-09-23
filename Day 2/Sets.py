s = {1, 2, 3, 2, 1}
print(s)   # {1, 2, 3}

# Add/Remove
s.add(4)
s.remove(2)
print(s)   # {1, 3, 4}

# Set operations
a = {1,2,3}
b = {3,4,5}
print(a | b)  # union {1,2,3,4,5}
print(a & b)  # intersection {3}
print(a - b)  # difference {1,2}