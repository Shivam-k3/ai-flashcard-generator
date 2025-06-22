# 🚀 OpenAI API Setup Guide

Follow these steps to enable real AI-powered flashcard generation:

## Step 1: Get Your OpenAI API Key

1. **Visit [OpenAI Platform](https://platform.openai.com/api-keys)**
2. **Sign in or create an account**
3. **Click "Create new secret key"**
4. **Copy the API key** (it starts with `sk-`)

## Step 2: Create Environment File

1. **In the `backend` folder**, create a new file called `.env`
2. **Add your API key** to the file:
   ```
   OPENAI_API_KEY=sk-your_actual_api_key_here
   ```

## Step 3: Restart the Backend

1. **Stop the current backend server** (Ctrl+C in terminal)
2. **Start it again**:
   ```bash
   cd backend
   python main.py
   ```

## Step 4: Test the Integration

1. **Open your frontend** at `http://localhost:3000`
2. **Upload a PDF** and click "Generate Flashcards"
3. **Check the response** - you should see `"ai_used": true` in the response

## 🔍 Verify Setup

Visit `http://localhost:8000/health` to check if your API key is configured correctly.

## 💡 Tips

- **Keep your API key secret** - never share it publicly
- **Monitor your usage** - OpenAI charges per API call
- **Start with small PDFs** - larger files use more tokens

## 🆘 Troubleshooting

If you see mock flashcards instead of AI-generated ones:
1. Check that your `.env` file is in the `backend` folder
2. Verify your API key is correct
3. Restart the backend server
4. Check the `/health` endpoint for status 