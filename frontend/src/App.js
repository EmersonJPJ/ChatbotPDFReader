import { useState, useRef } from 'react';
import ChatBox from './components/ChatBox';
import InputBar from './components/InputBar';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const eventSourceRef = useRef(null);

  const handleSend = async (message) => {
    if (!message.trim() || loading) return;

    const userMessage = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.type === 'content') {
                setMessages(prev => {
                  const updated = [...prev];
                  const last = updated[updated.length - 1];

                  if (!last.content.endsWith(data.content)) {
                    last.content += data.content;
                  }

                  return updated;
                });
              } else if (data.type === 'done') {
                setLoading(false);
              } else if (data.type === 'error') {
                addErrorMessage(data.content);
                setLoading(false);
              }
            } catch (error) {
              console.error('Error parsing SSE data:', error);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      addErrorMessage('Failed to connect to server');
      setLoading(false);
    }
  };

  const addErrorMessage = (text) => {
    setMessages(prev => [...prev.slice(0, -1), { role: 'assistant', content: text }]);
  };

  const handleClear = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setMessages([]);
    setLoading(false);
  };

  return (
    <div className="app">
      <h1>PDF ChatBot</h1>
      <ChatBox messages={messages} loading={loading} />
      <InputBar 
        onSend={handleSend} 
        onClear={handleClear} 
        loading={loading} 
      />
    </div>
  );
}

export default App;
