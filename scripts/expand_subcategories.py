#!/usr/bin/env python3
import os, sys, openai
from tenacity import retry, stop_after_attempt, wait_exponential

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "25"))
RETRIES = int(os.getenv("RETRIES_PER_CAT", "2"))
BACKOFF_MAX = int(os.getenv("BACKOFF_MAX", "6"))

if len(sys.argv) < 2:
    print("Usage: python expand_subcategories.py <subject>")
    sys.exit(1)

subject = sys.argv[1]

@retry(stop=stop_after_attempt(RETRIES), wait=wait_exponential(multiplier=1, min=1, max=BACKOFF_MAX), reraise=True)
def call_openai(prompt):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You expand subjects into MECE subcategories."},
            {"role": "user", "content": prompt},
        ],
        timeout=HTTP_TIMEOUT,
    )
    return response["choices"][0]["message"]["content"].strip()

prompt = f"Expand the subject '{subject}' into a MECE list of subcategories. Output as bullet points."

print(call_openai(prompt))

