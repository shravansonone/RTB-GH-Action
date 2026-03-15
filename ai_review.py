import subprocess
import re

review = []

# Read diff file
with open("diff.txt") as f:
    diff = f.read()

# Find changed files
files = re.findall(r'\+\+\+ b/(.*)', diff)

if not files:
    review.append("No files changed.")

for file in files:

    # Check Python files
    if file.endswith(".py"):
        try:
            subprocess.check_output(["python", "-m", "py_compile", file], stderr=subprocess.STDOUT)
            review.append(f"{file} : Python syntax OK")
        except subprocess.CalledProcessError as e:
            review.append(f"{file} : Python syntax ERROR\n{e.output.decode()}")

    # Check YAML files
    elif file.endswith(".yaml") or file.endswith(".yml"):
        try:
            subprocess.check_output(["python", "-c", f"import yaml; yaml.safe_load(open('{file}'))"])
            review.append(f"{file} : YAML syntax OK")
        except Exception as e:
            review.append(f"{file} : YAML syntax ERROR\n{str(e)}")

    else:
        review.append(f"{file} : File type not checked")

# Write review result
with open("review.txt", "w") as f:
    f.write("\n\n".join(review))

print("Validation complete")
