from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
import json
from ai_service import stream_chat_response
import time
from collections import defaultdict

request_log = defaultdict(list)

MAX_REQUESTS_PER_MINUTE = 5
TIME_WINDOW_SECONDS = 60

#Function to check if an IP is rate-limited
def is_rate_limited(ip: str) -> bool:
    now = time.time()
    request_times = request_log[ip]

    # Keep only requests within the time window
    request_times = [t for t in request_times if now - t < TIME_WINDOW_SECONDS]
    request_log[ip] = request_times

    if len(request_times) >= MAX_REQUESTS_PER_MINUTE:
        return True

    request_log[ip].append(now)
    return False

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(request: Request):
    """Endpoint para chat con streaming response"""
    try:

        # Check rate limit for the IP address
        ip = request.client.host
        if is_rate_limited(ip):
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait before trying again.")


        data = await request.json()
        user_message = data.get("message")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        pdf_context = request.app.state.pdf_context
        
        if not pdf_context:
            raise HTTPException(status_code=500, detail="PDF context not loaded")

        # Event generator for streaming response
        async def event_generator():
            try:
                async for chunk in stream_chat_response(user_message, pdf_context):
                    if chunk.get("type") == "content" and chunk.get("content"):
                        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                    elif chunk.get("type") == "done":
                        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                    elif chunk.get("type") == "error":
                        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
            except Exception as e:
                print(f"Error in event generator: {e}")
                yield f"data: {json.dumps({'type': 'error', 'content': str(e)}, ensure_ascii=False)}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

