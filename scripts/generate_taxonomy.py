
#!/usr/bin/env python3
import os, sys, openai

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if len(sys.argv) < 2:
    print("Usage: python generate_taxonomy.py <subject>")
    sys.exit(1)

subject = sys.argv[1]

response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that creates taxonomies."},
        {"role": "user", "content": f"Generate a taxonomy of categories for '{subject}'."}
    ]
)

print(response["choices"][0]["message"]["content"])
