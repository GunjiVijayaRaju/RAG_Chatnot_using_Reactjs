import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { FaPlus, FaTrash  } from "react-icons/fa";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import "./index.css";
import "./index_copy.css"

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [tabIndex, setTabIndex] = useState(0);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    async function clearFiles() {
      try {
        const response = await axios.post("http://localhost:8000/delete-all-files");
        console.log("Deleted files:", response.data.files);
        setSelectedFiles([]); // Clear frontend state
      } catch (error) {
        console.error("Error clearing files:", error);
      }
    }

    clearFiles();

    chatBoxRef.current?.scrollTo({
      top: chatBoxRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, []);



  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get("http://localhost:8000/files");
        setSelectedFiles(response.data.files);
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    };
    fetchFiles();
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/chat", { message: input });
      const botMessage = { sender: "bot", text: response.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [...prev, { sender: "bot", text: "⚠️ Error: Unable to fetch response." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(response.data.message);
      setSelectedFiles((prev) => [...prev, file.name]);
    } catch (error) {
      console.error("File upload error:", error);
      alert("⚠️ Error: Unable to upload file.");
    }
  };

  const handleFileDelete = async (fileName) => {
    try {
      await axios.delete(`http://localhost:8000/delete-file/${fileName}`);
      setSelectedFiles((prev) => prev.filter((file) => file !== fileName));
    } catch (error) {
      console.error("Error deleting file:", error);
      alert("⚠️ Error: Unable to delete file.");
    }
  };




    // Function to render Markdown with code block enhancements
    const renderMarkdown = (text) => {
      const parts = text.split(/(```[\s\S]*?```)/g);
  
      return parts.map((part, index) => {
        if (part.startsWith("```") && part.endsWith("```")) {
          const codeContent = part.slice(3, -3); // Remove the triple backticks
          return (
            <div key={index} className="code-block">
              <button
                className="copy-button"
                onClick={() => navigator.clipboard.writeText(codeContent)}
              >
                📋 Copy
              </button>
              <pre>
                <code>{codeContent}</code>
              </pre>
            </div>
          );
        } else {
          return <ReactMarkdown key={index} remarkPlugins={[remarkGfm]}>{part}</ReactMarkdown>;
        }
      });
    };

    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
      setIsSidebarOpen(!isSidebarOpen);
    };  

  return (
    <>
       {/* <div className="chat-header">
            <h2>Chatbot</h2>
       </div>
      <Tabs selectedIndex={tabIndex} onSelect={(index) => setTabIndex(index)}>
        <TabList>
          <div className="tabs">
            <Tab>Chat</Tab>
            <Tab>Uploaded Files</Tab>
            </div>
        </TabList> */}

        <div className="relative flex">
            {/* Sidebar */}
            {isSidebarOpen && (
              <div className="absolute left-0 h-full w-64 shadow-lg bg-white">
                <button onClick={toggleSidebar} className="absolute right-0 top-0 border-l border-gray-300 p-2 text-lg focus:outline-none focus:ring-0 bg-transparent">✖</button>
                <ul className="mt-10 space-y-4 p-4">
                  <li><a href="/option1">Option 1</a></li>
                  <li><a href="/option2">Option 2</a></li>
                  <li><a href="/option3">Option 3</a></li>
                </ul>
              </div>
            )}
         <div className={`flex-1 transition-all duration-300 ${isSidebarOpen ? 'ml-64' : 'ml-0'}`}>
          <div className="chat-header flex justify-between items-center p-4 shadow-md"> 
            <h2 className="ml-auto">Chatbot</h2>
            {/* /*menu bar logiv*/ }
            <button onClick={toggleSidebar} className="absolute left-2 text-lg focus:outline-none focus:ring-0 bg-transparent">☰</button>
          </div>
          <Tabs selectedIndex={tabIndex} onSelect={(index) => setTabIndex(index)}>
            <TabList>
            <div className="tabs">
              <Tab>Chat</Tab>
              <Tab>Uploaded Files</Tab>
              </div>
            </TabList>  
          <TabPanel>
          <div className="chat-box" ref={chatBoxRef}>
            {messages.length === 0 && <p className="empty-message">Start a conversation...</p>}
            {messages.map((msg, index) => (
              <div key={index} className={msg.sender === "user" ? "user-message" : "bot-message"}>
                <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong>
                {renderMarkdown(msg.text)}
              </div>
            ))}
            {loading && <div className="bot-message">⏳ Bot is typing...</div>}
          </div>
            <div className="input-container">
              <label htmlFor="file-upload" className="file-upload-label">
                <div className="tooltip">
                  <FaPlus className="plus-icon" />
                  <span className="tooltip-text">Upload files here</span>
                </div>
                <input type="file" id="file-upload" onChange={handleFileChange} hidden />
              </label>
            
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a message..."
                disabled={loading}
                className="chat-input"
              />
              <button onClick={sendMessage} disabled={loading}>Send</button>
            </div>
          </TabPanel>

        
          <TabPanel>
            <div className="uploaded-files">
              <h3 className="uploaded_headings">Uploaded Files:</h3>
              <ul className="file-list">
                {selectedFiles.map((file, index) => (
                  <li key={index} className="file-item">
                    <span>{file}</span>
                    <button className="delete-button" onClick={() => handleFileDelete(file)}>
                      <FaTrash />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </TabPanel>
      </Tabs>
        {/* <button onClick={toggleSidebar} className="absolute left-2 top-2">Menu</button> */}
     </div>
    </div>
    </>
  );
};


// new code



export default Chatbot;
