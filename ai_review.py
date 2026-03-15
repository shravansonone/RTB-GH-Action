import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Read diff file
with open("diff.txt") as f:
    diff = f.read()

diff = diff[:4000]

prompt = f"""
You are a senior software engineer.

Review the following code changes and identify:
- syntax errors
- YAML mistakes
- Python issues
- bad practices

Code changes:
{diff}

Provide clear review comments.
"""

payload = {
    "inputs": prompt
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, list):
        review = result[0]["generated_text"]
    else:
        review = f"AI response error: {result}"

except Exception as e:
    review = f"AI review failed: {e}"

with open("review.txt", "w") as f:
    f.write(review)

print("AI review completed")
