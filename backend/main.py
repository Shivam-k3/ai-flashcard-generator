from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import io
import os
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow requests from your deployed frontend
CORS(app, resources={r"/*": {"origins": "https://ai-flashcard-generator-daz9.vercel.app"}})

# Configure Google Gemini
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        API_KEY_CONFIGURED = True
    else:
        model = None
        API_KEY_CONFIGURED = False
except Exception as e:
    model = None
    API_KEY_CONFIGURED = False
    print(f"Error configuring Google Gemini: {e}")

def extract_text_from_pdf(pdf_file: bytes) -> str:
    """Extract text content from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def get_mock_flashcards():
    """Return a list of mock flashcards for testing"""
    return [
        {"question": "What is the main topic of this document?", "answer": "This appears to be a study material or textbook content."},
        {"question": "How many pages does this document have?", "answer": "The document contains multiple pages of content."},
        {"question": "What type of content is this?", "answer": "This appears to be educational or academic content."},
        {"question": "What should you focus on when studying this material?", "answer": "Focus on understanding the key concepts and main ideas presented."},
        {"question": "How can you best learn from this content?", "answer": "Create your own notes, practice with flashcards, and review regularly."}
    ]

def generate_flashcards_with_ai(text: str, num_cards: int = 5) -> List[Dict[str, str]]:
    """Generate flashcards using Google Gemini"""
    if not API_KEY_CONFIGURED or not model:
        # Return mock flashcards if no API key is configured
        return get_mock_flashcards()
    
    try:
        # Truncate text if it's too long for the API
        max_chars = 30000  # Gemini has a larger context window
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        prompt = f"""
        Based on the following text, generate {num_cards} educational flashcards in a valid JSON array format.
        Each object in the array should have a "question" key and an "answer" key.
        
        Text content:
        {text}
        
        Generate the flashcards in this exact JSON format:
        [
            {{"question": "Your question here", "answer": "Your answer here"}},
            {{"question": "Your question here", "answer": "Your answer here"}}
        ]
        
        Do not include any text or formatting outside of the JSON array.
        """
        
        response = model.generate_content(prompt)
        
        # Parse the response
        content = response.text.strip()
        
        # Try to extract JSON from the response
        try:
            # Remove any markdown formatting if present
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            flashcards = json.loads(content)
            
            # Validate the structure
            if not isinstance(flashcards, list):
                raise ValueError("Response is not a list")
            
            for card in flashcards:
                if not isinstance(card, dict) or "question" not in card or "answer" not in card:
                    raise ValueError("Invalid flashcard structure")
            
            return flashcards
            
        except (json.JSONDecodeError, ValueError) as e:
            # If JSON parsing fails, return mock flashcards
            print(f"Error parsing AI response: {e}")
            return get_mock_flashcards()
            
    except Exception as e:
        print(f"Error calling Google Gemini API: {e}")
        # Return mock flashcards on error
        return get_mock_flashcards()

@app.route('/')
def root():
    """Health check endpoint"""
    return jsonify({"message": "AI Flashcard Generator API is running!"})

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """Upload PDF and generate flashcards"""
    
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']

        # Get number of cards from form, default to 5
        try:
            num_cards = int(request.form.get('num_cards', 5))
            # Clamp the value to a safe range to prevent abuse
            num_cards = max(1, min(20, num_cards))
        except (ValueError, TypeError):
            num_cards = 5
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        # Read the uploaded file
        pdf_content = file.read()
        
        # Check file size (limit to 10MB)
        if len(pdf_content) > 10 * 1024 * 1024:
            return jsonify({"error": "File size must be less than 10MB"}), 400
        
        # Extract text from PDF
        text_content = extract_text_from_pdf(pdf_content)
        
        if not text_content.strip():
            return jsonify({"error": "No text content found in PDF"}), 400
        
        # Generate flashcards using AI
        flashcards = generate_flashcards_with_ai(text_content, num_cards=num_cards)
        
        return jsonify({
            "message": "Flashcards generated successfully!",
            "filename": file.filename,
            "text_length": len(text_content),
            "flashcards": flashcards,
            "ai_used": API_KEY_CONFIGURED
        })
        
    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "ai_configured": API_KEY_CONFIGURED,
        "api_key_status": "configured" if API_KEY_CONFIGURED else "not_configured"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 