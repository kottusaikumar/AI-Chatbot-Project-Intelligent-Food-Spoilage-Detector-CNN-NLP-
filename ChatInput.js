import React, { useState, useRef } from 'react';

export default function ChatInput({ onSendMessage, loading, onUploadImage }) {
  const [inputText, setInputText] = useState("");
  const fileInputRef = useRef();

  function handleSend() {
    if (!inputText.trim() || loading) return;
    onSendMessage(inputText.trim());
    setInputText('');
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (file) {
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('File size too large. Please choose a file under 10MB.');
        return;
      }
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file.');
        return;
      }
      
      onUploadImage(file);
    }
    // Reset the input so the same file can be uploaded again if needed
    fileInputRef.current.value = "";
  }

  function handleUploadClick() {
    fileInputRef.current?.click();
  }

  return (
    <div className="chat-input-container">
      <input
        className="chat-input"
        placeholder="Send a message to chatbot"
        value={inputText}
        onChange={e => setInputText(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
      />
      <button 
        className="send-button" 
        onClick={handleSend} 
        disabled={loading || !inputText.trim()}
      >
        {loading ? "..." : "Send"}
      </button>
      
      <input 
        type="file" 
        accept="image/*"
        style={{ display: 'none' }}
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      
      <button 
        className="send-button upload-button" 
        onClick={handleUploadClick}
        disabled={loading}
        title="Upload an image for food spoilage detection"
      >
        📷 Upload Image
      </button>
    </div>
  );
}