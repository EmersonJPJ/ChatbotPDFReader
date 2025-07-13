import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Backend/ai_service.py
# This file contains the AI service logic for handling chat requests with streaming responses
async def stream_chat_response(user_msg: str, pdf_context: str):
    """Genera respuesta streaming usando OpenAI con contexto del PDF"""
    try:
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful AI assistant that answers questions based on the provided document. 

Instructions:
- Answer questions accurately based on the document content
- If the user asks in Spanish, respond in Spanish
- If the user asks in English, respond in English
- Be clear and concise in your responses
- If information is not in the document, say so clearly

Document content:
{pdf_context}"""
            },
            {"role": "user", "content": user_msg}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
            max_tokens=500,
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.3
        )

        accumulated_content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                accumulated_content += content
                if content:
                    yield {
                        "type": "content",
                        "content": content
                    }

        yield {"type": "done"}

        # Token tracking and cost estimation
        usage_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.3
        )

        usage = usage_response.usage
        if usage:
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens
            cost = total_tokens * 0.0015 / 1000  # gpt-3.5-turbo ≈ $0.0015/1K tokens

            print(f"🔍 Token usage summary:")
            print(f"  - Prompt tokens: {prompt_tokens}")
            print(f"  - Completion tokens: {completion_tokens}")
            print(f"  - Total tokens: {total_tokens}")
            print(f"💰 Estimated cost: ${cost:.6f} USD")

    except Exception as e:
        yield {
            "type": "error",
            "content": f"Error generating response: {str(e)}"
        }
