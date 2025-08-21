import React from 'react';

export default function ChatMessage({ message, sender }) {
  return (
    <div className={sender === "user" ? "chat-message-user" : "chat-message-robot"}>
      {sender === "robot" && (
        <img
          src="/robot.png"
          width="50"
          className="chat-message-profile"
          alt="robot"
        />
      )}
      <div className="chat-message-text">
        {typeof message === "string" ? message : message}
      </div>
      {sender === "user" && (
        <img
          src="/user.png"
          width="50"
          className="chat-message-profile"
          alt="user"
        />
      )}
    </div>
  );
}
