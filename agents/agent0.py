from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

print(os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a computer specialist."},
        {"role": "user", "content": "Describe to me the latest graphic card options."},
    ]
)

# Extract the reply from the response
reply = response['choices'][0]['message']['content']

print(reply)