import subprocess
from transformers import pipeline

# Retrieve the latest commit summary
commit_summary = subprocess.run(
    ["git", "log", "-1", "--pretty=format:%h - %s"],
    capture_output=True, text=True
).stdout.strip()

# Set up the text generation pipeline using a free Hugging Face model
generator = pipeline("text-generation", model="distilgpt2")
prompt = f"Document the following commit changes in a detailed manner:\n{commit_summary}\nDocumentation:"
generated = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]

# Append the generated documentation to a log file
with open("documentation_log.txt", "a") as f:
    f.write(generated + "\n")

print("Documentation updated with Hugging Face output.")
