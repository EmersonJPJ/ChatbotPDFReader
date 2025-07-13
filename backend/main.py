from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chat_router import router as chat_router
from pdf_loader import load_pdf_context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading PDF context...")
pdf_context = load_pdf_context("Accessible_Travel_Guide_Partial.pdf")


app.state.pdf_context = pdf_context

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)