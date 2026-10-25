import os
import time
from openai import OpenAI

client = OpenAI(
    api_key="abs",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=30,
    max_retries=0,
)

models = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.7-flash-lite", "gemini-3.7-flash"]

for model in models:
    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "hi"}],
            reasoning_effort="low",
        )
        print(model, "->", round(time.time() - start, 1), "s")
    except Exception as e:
        print(model, "-> error after", round(time.time() - start, 1), "s:", str(e))