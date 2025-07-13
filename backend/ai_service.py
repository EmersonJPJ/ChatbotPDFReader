import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def stream_chat_response(user_msg: str, pdf_context: str):
    messages = [
        {
            "role": "system",
            "content": f"You are an AI assistant that answers questions based on the following document:\n{pdf_context}"
        },
        {"role": "user", "content": user_msg}
    ]

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )

    async for chunk in response:
        token = chunk.choices[0].delta.get("content")
        if token:
            yield token
