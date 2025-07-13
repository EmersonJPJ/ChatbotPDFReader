import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def stream_chat_response(user_msg: str, pdf_context: str):
    """Genera respuesta streaming usando OpenAI con contexto del PDF"""
    try:
        print(f"Processing message: {user_msg}")
        print(f"PDF context length: {len(pdf_context)} characters")
        
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
                print(f"Chunk: '{content}'")
                
                if content:
                    yield {
                        "type": "content",
                        "content": content
                    }
        
        print(f"Total response: {accumulated_content}") 
        
        yield {"type": "done"}
        
    except Exception as e:
        print(f"Error in AI service: {e}")
        yield {
            "type": "error",
            "content": f"Error generating response: {str(e)}"
        }