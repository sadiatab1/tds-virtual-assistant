import requests
import base64
import os

# File details
filename = "sample_thread.md"
filepath = os.path.join("markdown_files", filename)

# Read and encode the file
with open(filepath, "rb") as f:
    encoded_file = base64.b64encode(f.read()).decode("utf-8")

# API payload
payload = {
    "question": "Explain the post content",
    "filename": filename,
    "file": encoded_file
}

# Send POST request
response = requests.post("http://127.0.0.1:5000/api", json=payload)

# Print results
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Failed to parse response JSON:", e)
    print("Raw Response:", response.text)
