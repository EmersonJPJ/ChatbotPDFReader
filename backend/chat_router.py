from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
import json
from ai_service import stream_chat_response

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(request: Request):
    """Endpoint para chat con streaming response"""
    try:
        data = await request.json()
        user_message = data.get("message")
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        pdf_context = request.app.state.pdf_context
        
        if not pdf_context:
            raise HTTPException(status_code=500, detail="PDF context not loaded")

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

@router.get("/pdf-info")
async def get_pdf_info(request: Request):
    """Endpoint para verificar la información del PDF cargado"""
    try:
        pdf_context = request.app.state.pdf_context
        if not pdf_context:
            return {"error": "PDF context not loaded"}
        
        preview = pdf_context[:500] + "..." if len(pdf_context) > 500 else pdf_context
        
        return {
            "status": "loaded",
            "length": len(pdf_context),
            "preview": preview
        }
    except Exception as e:
        return {"error": str(e)}