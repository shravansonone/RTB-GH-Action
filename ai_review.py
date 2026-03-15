import openai

with open("diff.txt") as f:
    code = f.read()

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role":"system","content":"You are a senior software engineer reviewing code."},
        {"role":"user","content":f"Review this code and give suggestions:\n{code}"}
    ]
)

review = response['choices'][0]['message']['content']

with open("review.txt","w") as f:
    f.write(review)
