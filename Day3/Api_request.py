import requests
# get
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print(response.status_code) 
print(response.json())        


# post
payload = {"title": "foo", "body": "bar", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)

print(response.status_code) 
print(response.json())

# PUT (update)
update = {"title": "Updated Title"}
response = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=update)

# DELETE
response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code) 


try:
    with open("missing.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("File not found!")
    
try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)
    response.raise_for_status()   # raises error for 4xx/5xx codes
    data = response.json()
    print(data)
except requests.exceptions.Timeout:
    print("Request timed out!")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
