import React, { useState } from 'react';
import './InputBar.css';

const InputBar = ({ onSend, onClear, loading, onExport}) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form className="inputBar" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={loading}
        placeholder="Type your question..."
      />
      <button type="submit" disabled={loading}>Send</button>
      <button type="button" onClick={onClear}>Clear</button>
      <button className="export" onClick={onExport} disabled={loading}>Export conversation</button>

    </form>
  );
};

export default InputBar;
