import React, { useRef, useEffect } from 'react';
import './ChatComponent.css';
import ChatShortcutComponent from './ChatShortcutComponent/ChatShortcutComponent';
import ChatInputComponent from './ChatInputComponent/ChatInputComponent';
import ChatMessageComponent from './ChatMessageComponent/ChatMessageComponent';
import ChatHeaderComponent from './ChatHeaderComponent/ChatHeaderComponent';
import { ChatMessage } from '../../types/ChatMessageTypes';
import { MessageSource } from '../../enums/ChatEnums';
// import Plot from 'react-plotly.js';
// import { PlotlyData } from '../../types/ChatMessageTypes';

interface ChatComponentProps {
    chatMessages: ChatMessage[];
    chatShortcutsText: string[];
    sendMessage: (input: string) => void;
    // plotlyData?: PlotlyData | null;
}

const ChatComponent: React.FC<ChatComponentProps> = ({ chatMessages, chatShortcutsText, sendMessage }) => {
    const dummyElement = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (dummyElement.current) dummyElement.current.scrollIntoView({ behavior: 'smooth' });
    }, [chatMessages]);

    useEffect(() => {
        console.log("Updated Chat Messages:", chatMessages);
    }, [chatMessages]);

    const handleInput = (inputText: string) => {
        sendMessage(inputText);
    };

    return (
        <div className='chat-component'>
            <ChatHeaderComponent />
            <div className='chat-box'>
                <div className='messages-list'>
                    {chatMessages.map((chatMessage: ChatMessage, idx) => (
                        <div key={idx} className={chatMessage.messageSource === MessageSource.AI ? "ai-message" : "user-message"}>
                            <ChatMessageComponent inputMessage={chatMessage} />
                        </div>
                    ))}
                </div>   
                <div ref={dummyElement} /> {/* Dummy element to help scroll */}
            </div>
            <div className='inputs-container'>
                <div className='shortcuts-container'>
                    {chatShortcutsText.map((chatShortcutText, idx) => (
                        <ChatShortcutComponent key={idx} shortcutText={chatShortcutText} onClick={handleInput} />
                    ))}
                </div>
                <div className='chat-input-textarea'>
                    <ChatInputComponent onSubmit={handleInput} />
                </div>
            </div>
        </div>
    );
};

export default ChatComponent;
