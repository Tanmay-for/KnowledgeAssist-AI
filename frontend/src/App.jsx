import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useState } from "react";

import {
  Plus,
  MessageSquare,
  FolderOpen,
  Settings,
  BookOpen,
  PanelLeftClose,
  Sparkles,
  Send,
  Paperclip,
  GraduationCap,
  FlaskConical,
  Lightbulb,
  Network,
  FileText,
} from "lucide-react";

import { sendChat } from "./services/api";
import KnowledgeGraph from "./pages/KnowledgeGraph.jsx";
import Documents from "./pages/Documents.jsx";

import "./App.css";

function normalizeMarkdown(text) {
  return text.replace(/\\([\\`*_DIL0[\]()#+\-.!>])/g, "$1");
}

function App() {
  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState("simple");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activePage, setActivePage] = useState("chat");

  async function handleSend() {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((previous) => [
      ...previous,
      { role: "user", content: userQuestion },
    ]);

    setQuestion("");
    setLoading(true);
    setError("");

    try {
      const data = await sendChat(userQuestion, mode);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
          graphContext: data.graph_context || [],
        },
      ]);
    } catch (err) {
      setError(err.message || "Unable to get an answer.");
    } finally {
      setLoading(false);
    }
  }

  function handleNewChat() {
    setMessages([]);
    setQuestion("");
    setError("");
    setMode("simple");
    setActivePage("chat");
  }

  function handleSuggestion(text, selectedMode) {
    setQuestion(text);
    setMode(selectedMode);
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  const suggestions = [
    {
      icon: <BookOpen size={20} />,
      title: "Explain a concept",
      description: "Understand important topics in simple language.",
      question: "Explain the important concepts in my uploaded documents.",
      mode: "simple",
    },
    {
      icon: <GraduationCap size={20} />,
      title: "Exam preparation",
      description: "Get structured, exam-ready answers.",
      question: "Explain classes and objects in C++.",
      mode: "exam",
    },
    {
      icon: <FlaskConical size={20} />,
      title: "Lab assistance",
      description: "Understand practical concepts and programs.",
      question: "Explain the practical applications of OOP concepts.",
      mode: "lab",
    },
    {
      icon: <Lightbulb size={20} />,
      title: "Viva preparation",
      description: "Prepare with short and direct answers.",
      question: "What are the important OOP viva questions?",
      mode: "viva",
    },
  ];

  return (
    <div className="app-container">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <Sparkles size={23} />
          </div>

          <div className="brand-name">
            <h2>KnowledgeAssist</h2>
            <span>AI Knowledge Assistant</span>
          </div>
        </div>

        <button className="new-chat-btn" onClick={handleNewChat}>
          <Plus size={18} />
          New Chat
        </button>

        <div className="sidebar-menu">
          <p className="menu-label">WORKSPACE</p>

          <button
            className={`menu-item ${activePage === "chat" ? "active" : ""}`}
            onClick={() => setActivePage("chat")}
          >
            <MessageSquare size={18} />
            Chat
          </button>

          <button
            className={`menu-item ${activePage === "graph" ? "active" : ""}`}
            onClick={() => setActivePage("graph")}
          >
            <Network size={18} />
            Knowledge Graph
          </button>

          <button
            className={`menu-item ${
              activePage === "documents" ? "active" : ""
            }`}
            onClick={() => setActivePage("documents")}
          >
            <FolderOpen size={18} />
            Documents
          </button>

          <button className="menu-item">
            <Settings size={18} />
            Settings
          </button>
        </div>

        <div className="sidebar-bottom">
          <div className="user-profile">
            <div className="profile-avatar">AI</div>

            <div>
              <strong>Local AI Assistant</strong>
              <span>Running locally</span>
            </div>

            <PanelLeftClose size={17} />
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        <header className="topbar">
          <div>
            <h3>
              {activePage === "chat"
                ? "AI Assistant"
                : activePage === "graph"
                ? "Knowledge Graph"
                : "Documents"}
            </h3>

            <span>
              {activePage === "chat"
                ? "Ask questions from your documents"
                : activePage === "graph"
                ? "Explore concepts and their relationships"
                : "Upload and manage your documents"}
            </span>
          </div>

          <div className="status-indicator">
            <span className="status-dot"></span>
            Local AI
          </div>
        </header>

        {/* CHAT PAGE */}
        {activePage === "chat" && (
          <div className="chat-area">
            <section className="chat-content">
              {messages.length === 0 && (
                <div className="welcome-section">
                  <div className="welcome-icon">
                    <Sparkles size={30} />
                  </div>

                  <h1>
                    Welcome to <span>KnowledgeAssist AI</span>
                  </h1>

                  <p className="welcome-description">
                    Your intelligent document-based knowledge assistant. Upload
                    documents and ask questions to get context-based answers.
                  </p>

                  <div className="suggestion-grid">
                    {suggestions.map((item, index) => (
                      <button
                        className="suggestion-card"
                        key={index}
                        onClick={() =>
                          handleSuggestion(item.question, item.mode)
                        }
                      >
                        <div className="suggestion-icon">{item.icon}</div>

                        <h3>{item.title}</h3>
                        <p>{item.description}</p>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div className="message-list">
                {messages.map((message, index) => (
                  <div
                    className={
                      message.role === "user"
                        ? "user-message"
                        : "assistant-message"
                    }
                    key={index}
                  >
                    <strong>
                      {message.role === "user" ? "You" : "KnowledgeAssist AI"}
                    </strong>

                    <div className="markdown-content">
                      {message.role === "assistant" ? (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {normalizeMarkdown(message.content)}
                        </ReactMarkdown>
                      ) : (
                        <p>{message.content}</p>
                      )}
                    </div>

                    {message.role === "assistant" &&
                      message.sources?.length > 0 && (
                        <div className="sources">
                          <strong>Document Sources</strong>

                          {message.sources
                            .filter(
                              (source, index, array) =>
                                index ===
                                array.findIndex(
                                  (item) =>
                                    item.filename === source.filename &&
                                    item.page === source.page
                                )
                            )
                            .map((source, index) => (
                              <div
                                key={`${source.filename}-${source.page}-${index}`}
                              >
                                <FileText size={15} />
                                {source.filename} — Page {source.page}
                              </div>
                            ))}
                        </div>
                      )}
                  </div>
                ))}
              </div>
            </section>

            {loading && (
              <div className="loading-message">
                <span className="loader"></span>
                KnowledgeAssist AI is thinking...
              </div>
            )}

            {error && <div className="error-message">{error}</div>}

            <div className="chat-controls">
              <div className="mode-selector">
                <label htmlFor="answer-mode">Answer Mode:</label>

                <select
                  id="answer-mode"
                  value={mode}
                  onChange={(event) => setMode(event.target.value)}
                >
                  <option value="simple">Simple</option>
                  <option value="exam">Exam</option>
                  <option value="lab">Lab</option>
                  <option value="viva">Viva</option>
                  <option value="detailed">Detailed</option>
                </select>
              </div>

              <div className="input-container">
                <button
                  className="attach-btn"
                  title="Document upload is available in Documents"
                  type="button"
                  onClick={() => setActivePage("documents")}
                >
                  <Paperclip size={20} />
                </button>

                <textarea
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask anything about your uploaded documents..."
                  rows={1}
                />

                <button
                  className="send-btn"
                  onClick={handleSend}
                  disabled={!question.trim() || loading}
                  title="Send message"
                >
                  <Send size={19} />
                </button>
              </div>

              <p className="input-footer">
                KnowledgeAssist AI uses RAG and local AI models. Answers are
                based on retrieved document context.
              </p>
            </div>
          </div>
        )}

        {/* KNOWLEDGE GRAPH PAGE */}
        {activePage === "graph" && <KnowledgeGraph />}

        {/* DOCUMENTS PAGE */}
        {activePage === "documents" && <Documents />}

        {/* SETTINGS PLACEHOLDER */}
        {activePage === "settings" && (
          <div className="chat-area">
            <div className="welcome-section">
              <div className="welcome-icon">
                <Settings size={30} />
              </div>
              <h1>Settings</h1>
              <p className="welcome-description">
                Settings will be available in a future update.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
