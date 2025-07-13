import React from 'react';
import Message from './Message';
import './ChatBox.css';

const ChatBox = ({ messages, loading }) => {
  return (
    <div className="chat-container">
      <div className="chat-history">
        {messages.map((msg, index) => (
          <Message key={index} type={msg.role} content={msg.content} />
        ))}
        {loading && <div className="typing-indicator">AI is typing...</div>}
      </div>
    </div>
  );
};

export default ChatBox;
