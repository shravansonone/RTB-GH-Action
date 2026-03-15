import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Read PR diff
try:
    with open("diff.txt") as f:
        diff = f.read()
except:
    diff = "No code diff found."

# Limit size
diff = diff[:4000]

prompt = f"""
You are a senior DevOps engineer reviewing a pull request.

Review the following code changes and give suggestions:

{diff}
"""

payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 300
    }
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    review = result[0]["generated_text"]

except Exception as e:
    review = f"AI review failed: {e}"

with open("review.txt", "w") as f:
    f.write(review)

print("AI review completed")
