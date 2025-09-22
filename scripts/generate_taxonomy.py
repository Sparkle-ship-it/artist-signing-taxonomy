#!/usr/bin/env python3
import os, sys
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ ERROR: Missing OPENAI_API_KEY. Add it to GitHub Secrets.", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=api_key)

if len(sys.argv) < 2:
    print("Usage: python generate_taxonomy.py <subject>")
    sys.exit(1)

subject = sys.argv[1]

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates taxonomies."},
            {"role": "user", "content": f"Generate a taxonomy of categories for '{subject}'."}
        ]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"❌ ERROR during API call: {e}", file=sys.stderr)
    sys.exit(1)
