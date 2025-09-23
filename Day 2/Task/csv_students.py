import csv
#  """
#     Read a CSV file of students (name, age) and return a list of dictionaries.
#     """
def read_students_csv(filename):
   
    students = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append({
                    'name': row['name'],
                    'age': int(row['age'])
                })
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except ValueError:
        print("Error: Invalid age value in CSV file.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return students

def main():
    # Read the CSV file
    students = read_students_csv('students.csv')
    
    if not students:
        print("No student data available.")
        return
    
    # Use list comprehension to get names of students older than 18
    names_older_than_18 = [student['name'] for student in students if student['age'] > 18]
    
    # Print the results
    print("Students older than 18:")
    if names_older_than_18:
        for name in names_older_than_18:
            print(f"- {name}")
    else:
        print("No students older than 18 found.")
    
    # Optional: Show all students with ages for reference
    print("\nAll students:")
    for student in students:
        print(f"- {student['name']}: {student['age']} years old")

if __name__ == "__main__":
    main()