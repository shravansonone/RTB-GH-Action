import os
import requests

# Hugging Face token from GitHub secret
HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Read diff file
try:
    with open("diff.txt", "r") as f:
        diff = f.read()
except:
    diff = "No diff found."

# Limit size so API does not reject request
diff = diff[:4000]

prompt = f"""
You are a senior software engineer reviewing a pull request.

Check the following code changes and identify:
- syntax errors
- Python issues
- YAML mistakes
- bad practices

Provide clear review comments.

Code changes:
{diff}
"""

payload = {
    "inputs": prompt
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)

    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    if response.status_code != 200:
        review = f"AI request failed with status {response.status_code}\n{response.text}"
    else:
        result = response.json()

        if isinstance(result, list):
            review = result[0].get("generated_text", "AI returned no review.")
        else:
            review = f"AI response error: {result}"

except Exception as e:
    review = f"AI review failed: {str(e)}"

# Write review result
with open("review.txt", "w") as f:
    f.write(review)

print("Review written to review.txt")
