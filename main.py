from dotenv import load_dotenv
import os
from openai import OpenAI

# .env読み込み
load_dotenv()

# APIキー取得
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("English Bot started! Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful English conversation partner."},
            {"role": "user", "content": user_input}
        ]
    )

    print("AI:", response.choices[0].message.content)