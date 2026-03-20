import uvicorn
from fastapi import Request, FastAPI
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

app = FastAPI()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/trigger_message")
async def n8n_handler(request:Request):
    """Роут для обработки входящего текста из чата"""
    try:
        req_data = await request.json()

        user_input = req_data.get("text")

        completion = await client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник."},
                {"role": "user", "content": user_input}
            ]
        )

        ai_response = completion.choices[0].message.content

        return {"answer" : ai_response}
    except Exception as exc:
        print(f"Ошибка {exc}")
        raise Exception(f'Что-то пошло не так при запросе: {exc}')


if __name__ == "__main__":
    uvicorn.run("chat_trigger_message:app", host="0.0.0.0", port=8000, reload=True)