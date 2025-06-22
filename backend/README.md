# AI Flashcard Generator Backend

This is the FastAPI backend for the AI Flashcard Generator application.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API (Optional)
To use real AI-generated flashcards, you need an OpenAI API key:

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_actual_api_key_here
```

**Note:** If you don't have an API key, the app will use mock flashcards for demonstration.

### 3. Run the Server
```bash
python main.py
```

The server will start on `http://localhost:8000`

### 4. API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /upload-pdf` - Upload PDF and generate flashcards

### 5. Test the API

You can test the API using the FastAPI docs at:
`http://localhost:8000/docs`

## Features

- ✅ PDF text extraction
- ✅ AI-powered flashcard generation (with OpenAI GPT)
- ✅ Fallback to mock flashcards if no API key
- ✅ CORS enabled for frontend integration
- ✅ File size and type validation
- ✅ Error handling and validation 