# PDF ChatBot 🤖📄

A full-stack AI-powered chatbot application that enables users to have intelligent conversations about the content of a PDF document. Built with React frontend and FastAPI backend, featuring real-time streaming responses and comprehensive conversation management.

## 🚀 Features

### Core Functionality
- **PDF Document Analysis**: Upload and analyze PDF documents for context-aware responses
- **Real-time Streaming**: Server-Sent Events (SSE) for live response streaming
- **Multilingual Support**: Responds in the same language as the user's query (Spanish/English)
- **Context-Aware Responses**: AI stays focused on PDF content only

### User Experience
- **Clean, Responsive Interface**: Modern React UI with intuitive design
- **Real-time Typing Indicators**: Visual feedback during AI response generation
- **Conversation Export**: Export chat history to Markdown format
- **Smart Button States**: Disabled buttons when not functional to prevent errors

### Technical Features
- **Rate Limiting**: Backend protection against abuse (5 requests/minute per IP)
- **Token & Cost Tracking**: Monitor API usage and estimated costs
- **Error Handling**: Comprehensive error management throughout the application
- **CORS Support**: Proper cross-origin resource sharing configuration

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework for APIs
- **OpenAI GPT-3.5-turbo**: AI model for intelligent responses
- **pdfplumber**: Advanced PDF text extraction
- **Server-Sent Events (SSE)**: Real-time streaming responses

### Frontend
- **React**: Modern JavaScript library for UI
- **Fetch API**: HTTP client for backend communication
- **CSS3**: Custom styling for responsive design

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- OpenAI API Key

## 🔧 Installation & Setup

### Backend Setup

1. **Clone the repository and navigate to backend directory**
```bash
git clone https://github.com/EmersonJPJ/ChatbotPDFReader
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Add your PDF document**
Place your PDF file in the backend directory and update the filename in `main.py`:
```python
pdf_context = load_pdf_context("your_document.pdf")
```

6. **Run the backend server**
```bash
python main.py
```
Server will start on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm start
```
Frontend will be available at `http://localhost:3000`

## 🏗️ Architecture & Workflow

### System Architecture
```
┌─────────────────┐    HTTP/SSE    ┌─────────────────┐    OpenAI API    ┌─────────────┐
│                 │──────────────→ │                 │─────────────────→│             │
│  React Frontend │                │ FastAPI Backend │                  │ OpenAI GPT  │
│                 │←────────────── │                 │←─────────────────│             │
└─────────────────┘   Streaming    └─────────────────┘    AI Response   └─────────────┘
```

### Data Flow

1. **Initialization**
   - Backend loads PDF context using `pdfplumber`
   - PDF text is cleaned and stored in application state
   - Frontend initializes with empty chat state

2. **User Interaction**
   - User types question in React input component
   - Frontend validates input and shows loading state
   - HTTP POST request sent to `/chat` endpoint

3. **Backend Processing**
   - Rate limiting check for user IP
   - Message validation and PDF context retrieval
   - AI service constructs system prompt with PDF context
   - OpenAI API called with streaming enabled

4. **Response Streaming**
   - AI response chunks streamed via Server-Sent Events
   - Frontend processes each chunk in real-time
   - UI updates incrementally as response builds

5. **Completion**
   - Token usage and cost tracking logged
   - Final response state updated
   - User can continue conversation or export

## 📁 Project Structure

```
ChatBotPDFReader/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── chat_router.py       # Chat endpoint with rate limiting
│   ├── pdf_loader.py        # PDF processing utilities
│   ├── ai_service.py        # OpenAI integration & streaming
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main application component
│   │   ├── components/
│   │   │   ├── ChatBox.jsx     # Chat history display
│   │   │   ├── InputBar.jsx    # Message input & controls
│   │   │   └── Message.jsx     # Individual message component
│   │   │   └── Message.css     # Style
│   │   │   └── InputBar.css    # Style
│   │   │   └── ChatBox.css     # Style
│   └── package.json        # Node.js dependencies
└── README.md
└── .gitignore
```


## 🎯 API Endpoints

### `POST /chat`
Handles chat requests with streaming responses.

**Request:**
```json
{
  "message": "What does the document say about accessibility?"
}
```

**Response:** Server-Sent Events stream
```
data: {"type": "content", "content": "According to the document..."}
data: {"type": "content", "content": " accessibility features include..."}
data: {"type": "done"}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## 🎨 UI Components

### ChatBox Component
- Displays conversation history
- Shows typing indicators
- Handles message rendering
- Auto-scrolls to latest messages

### InputBar Component
- Message input with validation
- Send/Clear/Export buttons
- Smart button state management
- Form submission handling

### Message Component
- Individual message display
- User vs AI message styling
- Content formatting
- Responsive design

## 📊 Performance Features

### Rate Limiting
- **5 requests per minute** per IP address
- **Sliding window** implementation
- **Memory efficient** with automatic cleanup
- **429 status code** for exceeded limits

### Token Tracking
- **Real-time monitoring** of API usage
- **Cost estimation** for budget management
- **Detailed logging** of token consumption
- **Per-request metrics** tracking

### Error Handling
- **Comprehensive try-catch** blocks
- **User-friendly error messages**
- **Graceful degradation** on failures
- **Connection recovery** mechanisms

## 🚦 Usage Examples

### Basic Query
```
User: "What are the main topics covered in this document?"
AI: "Based on the document, the main topics include..."
```

### Multilingual Support
```
User: "¿Cuáles son los puntos principales del documento?"
AI: "Según el documento, los puntos principales incluyen..."
```

### Export Feature
Users can export conversations as Markdown files with formatted timestamps and role indicators.

## 🔐 Security Considerations

- **API Key Protection**: Environment variables for sensitive data
- **Rate Limiting**: Prevents abuse and excessive API usage
- **Input Validation**: Sanitizes user inputs
- **CORS Configuration**: Controlled cross-origin access
- **Error Sanitization**: Prevents information leakage

## 🚀 Future Enhancements

- **Multiple PDF Support**: Handle multiple documents simultaneously
- **User Authentication**: Add user accounts and session management
- **Conversation Persistence**: Save chat history to database
- **Advanced Analytics**: Detailed usage statistics and insights

---

## 🤝 Contributing

Contributions are always welcome! If you have suggestions, improvements, or bug fixes, feel free to open an issue or create a pull request.

---


## ✨ Contact  

Feel free to reach out for any questions or suggestions!  

- 📧 **Email**: emerson04vade@gmail.com  
- 💻 **GitHub**: EmersonJPJ
