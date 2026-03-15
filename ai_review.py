import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Read diff
try:
    with open("diff.txt", "r") as f:
        diff = f.read()
except:
    diff = "No code changes found."

diff = diff[:4000]

payload = {
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "messages": [
        {
            "role": "system",
            "content": "You are a senior software engineer reviewing pull requests."
        },
        {
            "role": "user",
            "content": f"""
Review the following code changes and suggest improvements.
Focus on readability, best practices, and maintainability.

Code changes:
{diff}

Provide bullet point suggestions.
"""
        }
    ]
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        review = f"AI request failed ({response.status_code}):\n{response.text}"
    else:
        result = response.json()
        review = result["choices"][0]["message"]["content"]

except Exception as e:
    review = f"AI review failed: {str(e)}"

with open("review.txt", "w") as f:
    f.write(review)

print("AI suggestion review completed")
