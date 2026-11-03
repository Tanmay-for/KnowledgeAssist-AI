import { useState, useEffect, useCallback } from "react";
import {
  UploadCloud,
  FileText,
  File,
  CheckCircle,
  AlertCircle,
  LoaderCircle,
  RefreshCw,
  Trash2,
} from "lucide-react";

import { getDocuments } from "../services/api";

const API_BASE_URL = "http://127.0.0.1:8000";

function Documents() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [storageType, setStorageType] = useState("permanent");
  const [uploading, setUploading] = useState(false);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [deletingDocumentId, setDeletingDocumentId] = useState(null);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [uploadedDocuments, setUploadedDocuments] = useState([]);

  // Fetch saved documents from backend
  const fetchDocuments = useCallback(async () => {
    setLoadingDocuments(true);

    try {
      const documents = await getDocuments();
      setUploadedDocuments(documents);
      setError("");
    } catch (err) {
      setError("Unable to load saved documents: " + err.message);
    } finally {
      setLoadingDocuments(false);
    }
  }, []);

  // Load documents when page opens
  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  function handleFileChange(event) {
    const file = event.target.files[0];

    setMessage("");
    setError("");

    if (!file) return;

    const extension = file.name.split(".").pop().toLowerCase();

    if (!["pdf", "txt"].includes(extension)) {
      setError("Only PDF and TXT files are supported.");
      setSelectedFile(null);
      return;
    }

    if (file.size > 20 * 1024 * 1024) {
      setError("File size must not exceed 20 MB.");
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  }

  async function handleUpload() {
    if (!selectedFile || uploading) return;

    setUploading(true);
    setMessage("");
    setError("");

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("storage_type", storageType);

    try {
      const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setMessage(`${selectedFile.name} uploaded and indexed successfully!`);
      setSelectedFile(null);

      const fileInput = document.getElementById("document-file");
      if (fileInput) fileInput.value = "";

      await fetchDocuments();
    } catch (err) {
      setError(err.message || "Unable to upload document.");
    } finally {
      setUploading(false);
    }
  }

  // Delete document after user confirmation
  async function handleDelete(document) {
    if (deletingDocumentId || uploading) return;

    const confirmed = window.confirm(
      `Are you sure you want to delete "${document.original_filename}"?\n\nThis will remove its uploaded file, vector records, registry entry and Knowledge Graph contributions.`
    );

    if (!confirmed) return;

    setDeletingDocumentId(document.document_id);
    setMessage("");
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/documents/${encodeURIComponent(document.document_id)}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Document deletion failed.");
      }

      setMessage(`${document.original_filename} deleted successfully!`);

      await fetchDocuments();
    } catch (err) {
      setError(err.message || "Unable to delete document.");
    } finally {
      setDeletingDocumentId(null);
    }
  }

  function formatDate(dateString) {
    if (!dateString) return "Date unavailable";

    return new Date(dateString).toLocaleString();
  }

  return (
    <div className="documents-page">
      <div className="documents-header">
        <div>
          <h1>My Documents</h1>
          <p>Upload and manage your knowledge base documents.</p>
        </div>
      </div>

      {/* Upload section */}
      <div className="upload-card">
        <div className="upload-heading">
          <div className="upload-icon">
            <UploadCloud size={25} />
          </div>

          <div>
            <h2>Upload Documents</h2>
            <p>Upload PDF or TXT files to your knowledge base.</p>
          </div>
        </div>

        <label htmlFor="document-file" className="upload-dropzone">
          <UploadCloud size={42} />
          <h3>Click to select a document</h3>
          <p>PDF or TXT · Maximum size 20 MB</p>

          <input
            id="document-file"
            type="file"
            accept=".pdf,.txt"
            onChange={handleFileChange}
          />
        </label>

        {selectedFile && (
          <div className="selected-file">
            <FileText size={21} />

            <div>
              <strong>{selectedFile.name}</strong>
              <span>{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</span>
            </div>
          </div>
        )}

        <div className="storage-selection">
          <label htmlFor="storage-type">Storage Type</label>

          <select
            id="storage-type"
            value={storageType}
            onChange={(event) => setStorageType(event.target.value)}
          >
            <option value="permanent">Permanent Storage</option>
            <option value="temporary">Temporary Storage</option>
          </select>
        </div>

        <button
          className="upload-submit-btn"
          onClick={handleUpload}
          disabled={!selectedFile || uploading || deletingDocumentId !== null}
        >
          {uploading ? (
            <>
              <LoaderCircle size={19} />
              Processing Document...
            </>
          ) : (
            <>
              <UploadCloud size={19} />
              Upload Document
            </>
          )}
        </button>

        {message && (
          <div className="upload-success">
            <CheckCircle size={19} />
            {message}
          </div>
        )}

        {error && (
          <div className="upload-error">
            <AlertCircle size={19} />
            {error}
          </div>
        )}
      </div>

      {/* Uploaded documents section */}
      <div className="uploaded-documents-card">
        <div className="uploaded-heading">
          <h2>All Uploaded Documents</h2>

          <div>
            <span>{uploadedDocuments.length} documents</span>

            <button
              type="button"
              onClick={fetchDocuments}
              disabled={loadingDocuments || deletingDocumentId !== null}
              title="Refresh documents"
            >
              <RefreshCw size={17} />
            </button>
          </div>
        </div>

        {loadingDocuments ? (
          <div className="empty-documents">
            <LoaderCircle size={30} />
            <p>Loading documents...</p>
          </div>
        ) : uploadedDocuments.length === 0 ? (
          <div className="empty-documents">
            <File size={35} />
            <p>No documents found.</p>
          </div>
        ) : (
          uploadedDocuments.map((document) => {
            const isDeleting = deletingDocumentId === document.document_id;

            return (
              <div className="document-item" key={document.document_id}>
                <FileText size={23} />

                <div className="document-details">
                  <strong>{document.original_filename}</strong>

                  <span>
                    {document.total_pages} pages · {document.total_chunks}{" "}
                    chunks · {document.storage_type}
                  </span>

                  <span>Uploaded: {formatDate(document.upload_date)}</span>
                </div>

                {isDeleting ? (
                  <button
                    type="button"
                    className="delete-document-btn"
                    disabled
                  >
                    <LoaderCircle size={17} />
                    Deleting...
                  </button>
                ) : (
                  <>
                    <CheckCircle size={19} className="document-status-icon" />

                    <button
                      type="button"
                      className="delete-document-btn"
                      onClick={() => handleDelete(document)}
                      disabled={deletingDocumentId !== null || uploading}
                      title={`Delete ${document.original_filename}`}
                    >
                      <Trash2 size={17} />
                      Delete
                    </button>
                  </>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default Documents;
