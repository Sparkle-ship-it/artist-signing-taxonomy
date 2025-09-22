#!/usr/bin/env python3
import os, sys
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "25"))
RETRIES = int(os.getenv("RETRIES_PER_CAT", "2"))
BACKOFF_MAX = int(os.getenv("BACKOFF_MAX", "6"))

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: Missing OPENAI_API_KEY. Add it to GitHub Secrets.", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=api_key)

if len(sys.argv) < 2:
    print("Usage: python expand_subcategories.py <subject>")
    sys.exit(1)

subject = sys.argv[1]

@retry(
    stop=stop_after_attempt(RETRIES),
    wait=wait_exponential(multiplier=1, min=1, max=BACKOFF_MAX),
    reraise=True
)
def call_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You expand subjects into MECE subcategories."},
            {"role": "user", "content": prompt},
        ],
        timeout=HTTP_TIMEOUT,
    )
    return response.choices[0].message.content.strip()

prompt = f"Expand the subject '{subject}' into a MECE list of subcategories. Output as bullet points."

try:
    print(call_openai(prompt))
except Exception as e:
    print(f"❌ ERROR during API call: {e}", file=sys.stderr)
    sys.exit(1)
