import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Include CSS for styling

// Centralized API Endpoint
const API_BASE_URL = "https://d7ca-2406-7400-56-aa49-3868-8830-70ab-6dda.ngrok-free.app/answer"; // Update this with your ngrok or server URL

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]); // Store chat messages

  const handleInputChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async () => {
    if (question.trim()) {
      setLoading(true);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: question, sender: "user" },
      ]); // Append user message

      try {
        const res = await axios.post(
          API_BASE_URL,
          { question },
          { headers: { "Content-Type": "application/json" } }
        );

        const { specialty, answer } = res.data;

        // Validate response fields
        if (!specialty || !answer) {
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: "Sorry, I couldn't get a valid response. Please try again.", sender: "bot" },
          ]);
          return;
        }

        // Append bot response
        const fullResponse = `Specialty: ${specialty}\n\nAnswer: ${answer}`;
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: fullResponse, sender: "bot" },
        ]);
      } catch (error) {
        console.error("Error fetching answer:", error);
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            text: "There was an error fetching the answer. Please check your connection or try again later.",
            sender: "bot",
          },
        ]);
      } finally {
        setLoading(false);
        setQuestion(""); // Clear input after submission
      }
    }
  };

  const handleNewChat = () => {
    setMessages([]); // Clear all messages
    setQuestion(""); // Clear input field
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
