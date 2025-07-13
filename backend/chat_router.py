from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from ai_service import stream_chat_response

router = APIRouter()

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    pdf_context = request.app.state.pdf_context

    async def event_generator():
        async for chunk in stream_chat_response(user_message, pdf_context):
            yield {
                "event": "message",
                "data": {"type": "content", "content": chunk}
            }
        yield {
            "event": "message",
            "data": {"type": "done"}
        }

    return EventSourceResponse(event_generator())
