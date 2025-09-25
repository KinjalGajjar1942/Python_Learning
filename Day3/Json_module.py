import json

person = {"name": "Alice", "age": 25, "city": "New York"}
json_string = json.dumps(person)   # convert to JSON string
print(json_string)

data = '{"name":"Alice","age":25,"city":"New York"}'
parsed = json.loads(data)
print(parsed["name"]) 

# Save dict to file as JSON
with open("person.json", "w") as f:
    json.dump(person, f)
    
# Load JSON from file
with open("person.json", "r") as f:
    data = json.load(f)
    print(data)