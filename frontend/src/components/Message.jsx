import React from 'react';
import './Message.css';

const Message = ({ type, content }) => {
  return (
    <div className={`message ${type === 'user' ? 'user' : 'ai'}`}>
      <p>{content}</p>
    </div>
  );
};

export default Message;
