import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isRelevant, setIsRelevant] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/ask/', { question });
      setAnswer(response.data.answer);
      setIsRelevant(response.data.is_relevant);
    } catch (error) {
      setAnswer('Error: ' + error.message);
      setIsRelevant(true); // Default to true on error
    }
    setLoading(false);
  };

  return (

    <div className="App">
      <div className="top-bar">
        <div className="hamburger" onClick={() => setSidebarOpen(!sidebarOpen)}>
          &#9776; {/* Hamburger icon */}
        </div>
        <img src="./logo_uim.png" alt="logo" width="50" height="50" style={{ margin: '5px' }} />
        <img src="./sc.png" alt="logo" width="50" height="50" style={{ margin: '5px' }} />
        <img src="./yauim.png" alt="logo" width="50" height="50" style={{ margin: '5px' }} />
      </div>
      <div className="app-container">
        {sidebarOpen && (
          <div className="sidebar">
            {/* Sidebar content - e.g., navigation */}
            <h3>Menu</h3>
            <ul>
              <li>Home</li>
              <hr />
              <li>About</li>
              <hr />
              <li>Contact</li>
            </ul>
          </div>
        )}
        <div className="main-content">
          <header className="App-header">
            <h1 className= "App-title"> Selamat Datang di <span style={{ color: 'green', fontWeight: 'bold' }}>YaUIM</span></h1>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question..."
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Asking...' : 'Ask'}
              </button>
            </form>
            {answer && (
              <div className="answer">
                <h2>Answer:</h2>
                <p>{answer}</p>
                {!isRelevant && (
                  <div className="warning">
                    <small style={{ color: 'orange' }}>
                      ⚠️ Pertanyaan ini di luar lingkup kampus. Saya hanya bisa menjawab tentang informasi kampus YaUIM.
                    </small>
                  </div>
                )}
              </div>
            )}
          </header>
        </div>
      </div>
    </div>
  );
}

export default App;