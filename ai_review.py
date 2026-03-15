import os
from openai import OpenAI

# Get API key from GitHub Secrets
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Read the diff file generated in workflow
try:
    with open("diff.txt", "r") as f:
        code_diff = f.read()
except FileNotFoundError:
    code_diff = "No diff found."

# Limit input size (important for free tier)
MAX_CHARS = 6000
code_diff = code_diff[:MAX_CHARS]

prompt = f"""
You are a senior DevOps and software engineer.

Review the following pull request changes and provide:
- Possible bugs
- Code improvements
- Best practices
- Security concerns

PR Diff:
{code_diff}
"""

review_output = ""

try:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",   # lightweight model
        messages=[
            {"role": "system", "content": "You are an expert code reviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    review_output = response.choices[0].message.content

except Exception as e:
    review_output = f"""
AI review could not be completed.

Reason:
{str(e)}

Possible causes:
- API quota exceeded
- Invalid API key
- Network issue
"""

# Save review so GitHub Action can post it as PR comment
with open("review.txt", "w") as f:
    f.write(review_output)

print("AI review completed.")
