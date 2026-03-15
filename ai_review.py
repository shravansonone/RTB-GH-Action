import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Read diff
try:
    with open("diff.txt", "r") as f:
        diff = f.read()
except:
    diff = "No code changes detected."

# limit size
diff = diff[:4000]

prompt = f"""
You are a senior software engineer reviewing a pull request.

Look at the following code changes and provide helpful suggestions.

Focus on:
- code readability improvements
- better coding practices
- performance improvements
- security improvements
- maintainability suggestions

Do NOT say "no issues found".
Always provide at least a few suggestions.

Code changes:
{diff}

Respond with clear bullet point suggestions.
"""

payload = {
    "inputs": prompt
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        review = f"AI request failed ({response.status_code}):\n{response.text}"
    else:
        result = response.json()

        if isinstance(result, list):
            review = result[0].get("generated_text", "No suggestions generated.")
        else:
            review = f"AI response error: {result}"

except Exception as e:
    review = f"AI review failed: {str(e)}"

with open("review.txt", "w") as f:
    f.write(review)

print("Suggestion review completed")
