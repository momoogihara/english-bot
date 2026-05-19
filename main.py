import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# templates フォルダを指定
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,        # ← 1番目に「request=request」を指定する
        name="index.html"       # ← 2番目に「name="ファイル名"」を指定する
    )

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):

    messages = [
        {
            "role": "system",
            "content": """
        You are an English conversation teacher.

        Return ONLY a valid JSON object with the following keys:
        {
          "corrected_sentence": "The corrected English sentence.",
          "reply": "A natural, friendly conversational reply in English (1-2 sentences). Do not explain grammar here.",
          "explanation_en": "Grammar or vocabulary explanation in English.",
          "explanation_ja": "Grammar or vocabulary explanation in Japanese."
        }

        Rules:
        1. corrected_sentence:
        - Only provide the corrected English sentence
        - No explanation, no comments

        2. reply:
        - Natural conversational English ONLY
        - Do NOT explain grammar here
        - Must be like a friend chatting
        - 1–2 short sentences only

        3. explanation_en:
        - Explanation in English.

        4. explanation_ja:
        - Explanation in Japanese.

        Important:
        - Do NOT mix roles
        - Do NOT give grammar explanation in reply
        - Reply is ONLY conversation
        """
        },
        {
            "role": "user",
            "content": request.message
        }
    ]

    # モデル名を gpt-4o-mini に修正し、JSON Modeを有効化
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
    except Exception:
        # フロントのエンドポイント (data.explanation_ja) に合わせる
        return {
            "corrected_sentence": "Error",
            "reply": "Sorry, something went wrong.",
            "explanation_en": "JSON parse failed.",
            "explanation_ja": "JSONの解析に失敗しました。"
        }

    return result