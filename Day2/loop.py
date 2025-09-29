# For loop
for i in range(5):
    print(i)

# While loop
i = 0
while i < 5:
    print(i)
    i += 1

# Iterating over collections
lst = [10,20,30]
for item in lst:
    print(item)

d = {"a":1,"b":2}
for key, value in d.items():
    print(key, value)

s = {1,2,3}
for item in s:
    print(item)

t = (5,6,7)
for x in t:
    print(x)

# Enumerate (get index & value)
lst = ["a","b","c"]
for i, val in enumerate(lst):
    print(i, val)

# Zip (iterate multiple lists together)
names = ["Alice","Bob"]
ages = [25,30]
for name, age in zip(names, ages):
    print(name, age)
