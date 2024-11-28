import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Include CSS for styling

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);  // Store chat messages

  const handleInputChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async () => {
    if (question.trim()) {
      setLoading(true);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: question, sender: "user" }
      ]);  // Append user message

      try {
        const res = await axios.post(
          "http://127.0.0.1:8000/answer",  // API endpoint
          { question },
          { headers: { "Content-Type": "application/json" } }
        );

        // Ensure you handle both the specialty and answer fields
        const { specialty, answer } = res.data;

        if (!specialty || !answer) {
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: "Sorry, I couldn't get a valid response.", sender: "bot" }
          ]);
          return;
        }

        // Update response with the full answer
        const fullResponse = `Specialty: ${specialty}\n\nAnswer: ${answer}`;

        // Append bot response to chat
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: fullResponse, sender: "bot" }
        ]);
      } catch (error) {
        console.error("Error fetching answer", error);
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Error fetching answer", sender: "bot" }
        ]);
      } finally {
        setLoading(false);
        setQuestion("");  // Clear input after submission
      }
    }
  };

  const handleNewChat = () => {
    setMessages([]);  // Clear all messages
    setQuestion("");   // Clear input field
  };

  return (
    <div className="App">
      <div className="chat-container">
        <h1>Medical Chatbot</h1>

        <div className="chat-box">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-bubble ${message.sender === "user" ? "user" : "bot"}`}
            >
              {message.text}
            </div>
          ))}

          {loading && (
            <div className="chat-bubble bot typing">
              <span>...</span> Typing...
            </div>
          )}
        </div>

        <div className="input-container">
          <input
            type="text"
            placeholder="Ask a medical question..."
            value={question}
            onChange={handleInputChange}
            disabled={loading}
          />
          <button onClick={handleSubmit} disabled={loading || !question.trim()}>
            {loading ? "Loading..." : "Ask"}
          </button>
        </div>

        <button onClick={handleNewChat} className="new-chat-btn">
          New Chat
        </button>
      </div>
    </div>
  );
}

export default App;
