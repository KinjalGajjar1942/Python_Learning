# Open a file in read mode
import os
file_path = os.path.join(os.path.dirname(__file__), "example.txt")
file = open(file_path, "r")  # "r" = read
content = file.read()           # read entire file
print(content)
file.close()


# Automatically closes the file, even if an error occurs.
with open(file_path, "r") as file:
    content = file.read()
    print(content)

# Read line by line
with open(file_path, "r") as file:
    for line in file:
        print(line.strip())  # remove newline characters


# Write to a file
# "w" → Write mode
# "a" → Append mode
# Overwrite file
output_path = os.path.join(os.path.dirname(__file__), "output.txt")
with open(output_path, "w") as file:
    file.write("Hello, Python!\n")

# Append to file
with open(output_path, "a") as file:
    file.write("This line is added.\n")

