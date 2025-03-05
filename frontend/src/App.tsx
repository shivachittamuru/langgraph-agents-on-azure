import React, { useState, useEffect } from 'react';
import './App.css';

import ChatComponent from './components/ChatComponent/ChatComponent';
// import { UserInput } from './types/ChatServiceTypes';
// import { invoke_sql_agent } from './services/chatService';

import { stream_sql_agent } from './services/chatService';
import { MessageSource } from './enums/ChatEnums';
import { ChatMessage } from './types/ChatMessageTypes';
import { v4 as uuidv4 } from 'uuid';


function App() {
  const shortcutTexts: string[] = [
    `What are the names of popular albums in the database?`,
    `Find albums released by artists who have more than 5 albums.`,
    `Who are the top 5 employees who have made the most sales?`,
    `Can you list the top 5 most expensive tracks?`
  ]

  const [chatSessionUuid, setchatSessionUuid] = useState("");

  useEffect(() => {
    const newChatSessionUuid = uuidv4();
    setchatSessionUuid(newChatSessionUuid);
  }, []);

  const defaultMsg: ChatMessage = { message: '👋 Hello! Feel free to click on any sample question below or ask your own!', messageSource: MessageSource.AI };
  const [messages, setMessages] = useState<ChatMessage[]>([defaultMsg]);

  const addMessageToChat = (message: ChatMessage) => {
    setMessages((prevMessages: ChatMessage[]) => [...prevMessages, message]);
  }

  const sendMessage = async (inputText: string) => {
    try {
      addMessageToChat({ message: inputText, messageSource: MessageSource.Human });

      let aiMessage: ChatMessage = { message: '', messageSource: MessageSource.AI };
      addMessageToChat(aiMessage);

      stream_sql_agent(
        inputText,
        chatSessionUuid,
        (data) => {
          if (data.plotly_json) {
            aiMessage.plotlyJson = data.plotly_json;
          } else {
            aiMessage.message += data.content;
          }
          setMessages((prevMessages) => [...prevMessages]);
        },
        (error) => {
          aiMessage.message += `\nAn error has occurred, please try again.`;
          setMessages((prevMessages) => [...prevMessages]);
        }
      );
    } catch (error) {
      addMessageToChat({
        message: `An error has occurred, please try again.`,
        messageSource: MessageSource.AI,
      });
    }
  };

  return (
    <div className="App">
      <ChatComponent
        chatMessages={messages}
        chatShortcutsText={shortcutTexts}
        sendMessage={sendMessage}
      />
    </div>
  );
}

export default App;