import React, { useState, useRef } from 'react';
import apiClient from './api';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator, AttachmentButton, ConversationHeader, Avatar, Loader } from '@chatscope/chat-ui-kit-react';


const pollResult = async (taskId, setChatMessages) => {
  let attempts = 0;
  const interval = setInterval(async () => {
    try {
      const response = await apiClient.get(`/result/${taskId}`);
      if (response.data.status !== 'Pending') {
        clearInterval(interval);
        const { answer, file, paragraph } = response.data;
        if (answer || file || paragraph) {
          const newMessages = [];

          if (answer) {
            newMessages.push({
              message: answer,
              sender: 'ChatGPT',
              direction: 'incoming',
            });
          }

          if (paragraph) {
            newMessages.push({
              message: paragraph,
              sender: 'ChatGPT',
              direction: 'incoming',
            });
          }
          if (file) {
            newMessages.push({
              type: 'html',
              message: `<a href="${file}" target="_blank">Open file</a>`,
              sender: 'ChatGPT',
              direction: 'incoming',
              htmlContent: `<iframe src="${file}" width="100%" height="300px"></iframe>`,
            });
          }
          setChatMessages(prevMessages => [...prevMessages, ...newMessages]);
        } else {
          console.warn("No valid response data received");
        }

      }
    } catch (error) {
      console.error("Error fetching result:", error);
    }
    if (++attempts > 10) clearInterval(interval); // Timeout after 10 attempts
  }, 3000); // Poll every 3 seconds
};

function App() {
  const [chatMessages, setChatMessages] = useState([]);
  const [isChatbotTyping, setIsChatbotTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);


  const handleUserMessage = async (message) => {
    const newMessage = {
      message,
      direction: "outgoing",
      sender: "user"
    };
    setIsChatbotTyping(true);

    setChatMessages(prevMessages => [...prevMessages, newMessage]);

    try {
      const response = await apiClient.post("/ask", { question: message });
      const taskId = response.data.task_id;
      pollResult(taskId, setChatMessages);
      setIsChatbotTyping(false);
    } catch (error) {
      console.error("Error sending message:", error);
      setIsChatbotTyping(false);
      setChatMessages(prevMessages => [
        ...prevMessages,
        {
            message: "Error fetching result: " + error.response?.data?.message || "Unknown error",
            sender: "System",
            direction: "incoming"
        }
    ]);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    if (file) {
      setIsLoading(true);
      // Handle file upload
      const formData = new FormData();
      formData.append('files', file);

      try {
        const response = await apiClient.post('/documents', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        const successMessage = response.data.message;
        setIsLoading(false);
        setChatMessages(prevMessages => [
          ...prevMessages,
          {
            message: successMessage,
            sender: 'System',
            direction: 'incoming',
          }
        ]);
      } catch (error) {
        setIsLoading(false);
        console.error("Error uploading file:", error);
        setChatMessages(prevMessages => [
          ...prevMessages,
          {
            message: "Error uploading file: " + error.response?.data?.message || "Unknown error",
            sender: "System",
            direction: "incoming"
          }
        ]);
      }
    }
  };

  const triggerFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };


  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div style={{ position: "relative", height: "100vh", width: "700px" }}>
        <MainContainer>
          <ChatContainer>
            <ConversationHeader>
              <Avatar
                src="/robot_avatar.webp"
              />
              <ConversationHeader.Content
                info="ChatBot using OpenAI, where Users can ask questions related to the uploaded documents."
              />

            </ConversationHeader>
            <MessageList typingIndicator={isChatbotTyping ? <TypingIndicator content="GPT is thinking" /> : null}>
              {chatMessages.map((message, i) => (
                <Message key={i} model={message} style={message.sender === "ChatGPT" ? { textAlign: "left" } : {}} />
              ))}
            </MessageList>
            <div style={{ display: 'flex', alignItems: 'center', flexDirection: "row" }} as={MessageInput}>

              {isLoading && (<Loader variant="default" />)}
              <AttachmentButton onClick={triggerFileInput} />
              <MessageInput placeholder="Type message here..." onSend={handleUserMessage} attachButton={false}
                style={{
                  flexGrow: 1,
                  borderTop: 0,
                  flexShrink: "initial",
                }} />
              <input type="file" ref={fileInputRef} style={{ display: 'none' }} onChange={handleFileUpload} />

            </div>
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
}

export default App;
