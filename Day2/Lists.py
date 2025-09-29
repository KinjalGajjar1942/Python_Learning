# Lists are ordered, mutable collections.
lst = [1, 2, 3, 4, 5]

# Access
print(lst[0])   # 1
print(lst[-1])  # 5

# Modify
lst[0] = 10
print(lst)      # [10, 2, 3, 4, 5]

# Add/Remove
lst.append(6)
lst.insert(2, 99)
lst.remove(3)
print(lst)      # [10, 2, 99, 4, 5, 6]

# Iterate
for item in lst:
    print(item)
