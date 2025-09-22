#!/usr/bin/env python3
import os, sys
from openai import OpenAI

# Use env var or fallback to gpt-5-mini
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if len(sys.argv) < 2:
    print("Usage: python generate_taxonomy.py <subject>")
    sys.exit(1)

subject = sys.argv[1]

# Call GPT
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that creates taxonomies."},
        {"role": "user", "content": f"Generate a taxonomy of categories for '{subject}'."}
    ]
)

# Print result
print(response.choices[0].message.content)
