import React, { useState } from 'react';
import './App.css';

function App() {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [flashcards, setFlashcards] = useState([]);
  const [aiUsed, setAiUsed] = useState(false);
  const [fileInfo, setFileInfo] = useState(null);
  const [numCards, setNumCards] = useState(5);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    const pdfFile = files.find(file => file.type === 'application/pdf');
    
    if (pdfFile) {
      setSelectedFile(pdfFile);
    } else {
      alert('Please upload a PDF file');
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    } else {
      alert('Please select a PDF file');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('num_cards', numCards);
      
      const response = await fetch('http://localhost:8000/upload-pdf', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload PDF');
      }
      
      const data = await response.json();
      setFlashcards(data.flashcards);
      setAiUsed(data.ai_used || false);
      setFileInfo({
        filename: data.filename,
        textLength: data.text_length
      });
    } catch (error) {
      console.error('Error uploading PDF:', error);
      alert(`Error: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Flashcard Generator</h1>
        <p>Upload your PDF and get instant flashcards!</p>
      </header>

      <main className="App-main">
        {!isProcessing && flashcards.length === 0 && (
          <div className="upload-section">
            <div
              className={`upload-area ${isDragOver ? 'drag-over' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <div className="upload-content">
                <div className="upload-icon">📄</div>
                <h3>Upload your PDF</h3>
                <p>Drag and drop your PDF here, or click to browse</p>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                  id="file-input"
                />
                <label htmlFor="file-input" className="browse-button">
                  Browse Files
                </label>
              </div>
            </div>

            {selectedFile && (
              <div className="file-info">
                <p>Selected file: {selectedFile.name}</p>
                <div className="num-cards-selector">
                  <label htmlFor="num-cards-input">Number of Flashcards:</label>
                  <input
                    id="num-cards-input"
                    type="number"
                    value={numCards}
                    onChange={(e) => setNumCards(Math.max(1, Math.min(20, Number(e.target.value))))}
                    min="1"
                    max="20"
                  />
                </div>
                <button onClick={handleUpload} className="generate-button">
                  Generate Flashcards
                </button>
              </div>
            )}
          </div>
        )}

        {isProcessing && (
          <div className="processing-section">
            <div className="loading-spinner"></div>
            <h3>Processing your PDF...</h3>
            <p>This may take a few moments</p>
          </div>
        )}

        {flashcards.length > 0 && (
          <div className="flashcards-section">
            <h2>Generated Flashcards</h2>
            {fileInfo && (
              <div className="file-details">
                <p><strong>File:</strong> {fileInfo.filename}</p>
                <p><strong>Text Length:</strong> {fileInfo.textLength.toLocaleString()} characters</p>
                <p><strong>AI Used:</strong> {aiUsed ? '✅ Yes' : '❌ No (Mock Data)'}</p>
              </div>
            )}
            <div className="flashcards-grid">
              {flashcards.map((card, index) => (
                <div key={index} className="flashcard">
                  <div className="card-front">
                    <h4>Question {index + 1}</h4>
                    <p>{card.question}</p>
                  </div>
                  <div className="card-back">
                    <h4>Answer</h4>
                    <p>{card.answer}</p>
                  </div>
                </div>
              ))}
            </div>
            <button 
              onClick={() => {
                setFlashcards([]);
                setSelectedFile(null);
                setAiUsed(false);
                setFileInfo(null);
              }} 
              className="new-upload-button"
            >
              Upload Another PDF
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
