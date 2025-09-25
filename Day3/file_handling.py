# Open a file in read mode
file = open("example.txt", "r")  # "r" = read
content = file.read()           # read entire file
print(content)
file.close()


# Automatically closes the file, even if an error occurs.
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

# Read line by line
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())  # remove newline characters


# Write to a file
# "w" → Write mode
# "a" → Append mode
# Overwrite file
with open("output.txt", "w") as file:
    file.write("Hello, Python!\n")

# Append to file
with open("output.txt", "a") as file:
    file.write("This line is added.\n")

