from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# .env を読み込む
load_dotenv()
# OpenAI client
client = OpenAI()
# FastAPI app
app = FastAPI()
# static フォルダを公開
app.mount("/static", StaticFiles(directory="static"), name="static")

# トップページ
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# リクエストの型
class ChatRequest(BaseModel):
    message: str


# /chat API
@app.post("/chat")
def chat(request: ChatRequest):
# system prompt
# 会話履歴を保存する箱
    messages = [
        {
        "role": "system",
        "content": """
You are a professional English conversation teacher.

Your job is to help the user improve English and continue natural conversation.

When the user writes a sentence in English, always respond in the following format:

Corrected sentence:
- Rewrite the user's sentence using natural and correct English.
Reply:
- Respond as a friendly conversation partner (NOT a grammar teacher here).
- Use natural, conversational English.
- Make the conversation continue.
- Always include 1 follow-up question.

Explanation:
- Explain grammar or vocabulary mistakes in Japanese.
- If the sentence is already correct, say so and briefly explain.

Rules:
- Do NOT repeat the user's sentence in Reply.
- Keep Reply short (1–3 sentences).
- Be natural like a real conversation, not a textbook.
"""
    },
    {
            "role": "user",
            "content": request.message
        }
    ]

# print("English Bot is ready! (type 'exit' to quit)\n")

# while True:
#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         print("Goodbye!")
#         break

#     # userの発言を履歴に追加
#     messages.append({"role": "user", "content": user_input})

    # API呼び出し
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    ai_response = response.choices[0].message.content

    # # AIの返答も履歴に追加（超重要）
    # messages.append({"role": "assistant", "content": ai_response})

   # 結果を分割
    corrected_sentence = ""
    reply = ""
    explanation = ""

    current_section = None

    for line in ai_response.splitlines():
        line = line.strip()

        if line.startswith("Corrected sentence"):
            current_section = "corrected"
            continue
        elif line.startswith("Reply"):
            current_section = "reply"
            continue
        elif line.startswith("Explanation"):
            current_section = "explanation"
            continue

        # 先頭の "- " を削除
        if line.startswith("- "):
            line = line[2:]

        if not line:
            continue

        if current_section == "corrected":
            corrected_sentence += line + "\n"
        elif current_section == "reply":
            reply += line + "\n"
        elif current_section == "explanation":
            explanation += line + "\n"

    return {
        "corrected_sentence": corrected_sentence.strip(),
        "reply": reply.strip(),
        "explanation": explanation.strip()
    }