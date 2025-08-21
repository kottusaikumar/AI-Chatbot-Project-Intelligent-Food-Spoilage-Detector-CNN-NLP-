import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';

export default function ChatMessages({ chatMessages }) {
  const chatMessagesRef = useRef(null);

  useEffect(() => {
    const containerElem = chatMessagesRef.current;
    if (containerElem) {
      containerElem.scrollTop = containerElem.scrollHeight;
    }
  }, [chatMessages]);

  return (
    <div className="chat-message-container" ref={chatMessagesRef}>
      {chatMessages.map((msg) => (
        <ChatMessage
          key={msg.id}
          message={msg.message}
          sender={msg.sender}
        />
      ))}
    </div>
  );
}
