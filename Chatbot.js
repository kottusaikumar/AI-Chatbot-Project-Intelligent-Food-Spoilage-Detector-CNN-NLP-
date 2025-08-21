import React, { useState} from 'react';
import ChatInput from './ChatInput';
import ChatMessages from './ChatMessages';

export default function Chatbot() {
  const [chatMessages, setChatMessages] = useState([
    { message: 'Welcome! I can help with questions and food spoilage detection.', sender: 'robot', id: 1 }
  ]);
  const [loading, setLoading] = useState(false);

  // Backend URL - update this if your backend runs on a different port
  const API_BASE_URL = 'http://localhost:5000';

  const handleSendMessage = async (inputText) => {
    if (!inputText) return;
    
    const userMsg = { message: inputText, sender: 'user', id: crypto.randomUUID() };
    setChatMessages(msgs => [...msgs, userMsg]);
    setLoading(true);

    // Special case for image prompt
    if (
      ["food is spoiled", "my vegetables are rotten", "the food looks rotten", "my apple are rotten",
        "my banana are rotten", "my mango are rotten"].includes(inputText.toLowerCase())
    ) {
      setChatMessages(msgs => [...msgs, { 
        message: "Please upload an image for verification.", 
        sender: "robot", 
        id: crypto.randomUUID() 
      }]);
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ message: inputText })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        setChatMessages(msgs => [...msgs, { 
          message: `Error: ${data.error}`, 
          sender: "robot", 
          id: crypto.randomUUID() 
        }]);
      } else {
        setChatMessages(msgs => [...msgs, { 
          message: data.response || "I couldn't generate a response.", 
          sender: "robot", 
          id: crypto.randomUUID() 
        }]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      setChatMessages(msgs => [...msgs, { 
        message: "Sorry, I'm having trouble connecting to the server. Please make sure the backend is running.", 
        sender: "robot", 
        id: crypto.randomUUID() 
      }]);
    }
    setLoading(false);
  };

  const handleUploadImage = async (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setChatMessages(msgs => [...msgs, { 
        message: "Please upload a valid image file.", 
        sender: "robot", 
        id: crypto.randomUUID() 
      }]);
      return;
    }

    // Show uploaded image immediately
    setChatMessages(msgs => [...msgs, { 
      message: <img 
        src={URL.createObjectURL(file)} 
        alt="uploaded" 
        style={{ 
          maxWidth: '180px', 
          maxHeight: '180px',
          borderRadius: '8px', 
          marginBottom: '7px',
          objectFit: 'cover'
        }} 
      />, 
      sender: 'user', 
      id: crypto.randomUUID() 
    }]);

    // Show processing message
    const processingMsgId = crypto.randomUUID();
    setChatMessages(msgs => [...msgs, { 
      message: "Analyzing your image...", 
      sender: "robot", 
      id: processingMsgId 
    }]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/classify`, { 
        method: 'POST', 
        body: formData 
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Remove processing message and add result
      setChatMessages(msgs => {
        const filtered = msgs.filter(msg => msg.id !== processingMsgId);
        return [...filtered, { 
          message: data.result || "Unable to analyze the image.", 
          sender: 'robot', 
          id: crypto.randomUUID() 
        }];
      });

    } catch (error) {
      console.error('Image upload error:', error);
      // Remove processing message and add error
      setChatMessages(msgs => {
        const filtered = msgs.filter(msg => msg.id !== processingMsgId);
        return [...filtered, { 
          message: "Image upload failed. Please make sure the backend server is running and try again.", 
          sender: "robot", 
          id: crypto.randomUUID() 
        }];
      });
    }
  };

  return (
    <>
      <ChatMessages chatMessages={chatMessages} />
      <ChatInput 
        onSendMessage={handleSendMessage} 
        loading={loading} 
        onUploadImage={handleUploadImage} 
      />
    </>
  );
}