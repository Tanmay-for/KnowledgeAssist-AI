const API_BASE_URL = "http://127.0.0.1:8000";

// Check backend connection
export async function checkBackend() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
      throw new Error("Backend connection failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Backend Error:", error);
    return null;
  }
}

// Send question to the RAG chatbot
export async function sendChat(question, mode) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        mode: mode,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Chat request failed");
    }

    return data;
  } catch (error) {
    console.error("Chat API Error:", error);
    throw error;
  }
}

// Fetch Knowledge Graph data
export async function getKnowledgeGraph() {
  try {
    const response = await fetch(`${API_BASE_URL}/graph/`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Unable to load Knowledge Graph");
    }

    return data;
  } catch (error) {
    console.error("Knowledge Graph API Error:", error);
    throw error;
  }
}

// Fetch all registered documents
export async function getDocuments() {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Unable to load documents");
    }

    return data.documents;
  } catch (error) {
    console.error("Documents API Error:", error);
    throw error;
  }
}
