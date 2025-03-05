import React, { useState, KeyboardEvent } from 'react';
import './ChatInputComponent.css';

interface ChatInputComponentProps {
  onSubmit: (inputText: string) => void
};

const ChatInputComponent = ({ onSubmit }: ChatInputComponentProps) => {
  const [inputText, setInputText] = useState('');
  const handleInputChange = (inputValue: string) => {
    setInputText(inputValue)
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      onSubmit(inputText);
      setInputText('')
    }
  }

  const onFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit(inputText);
    setInputText('')
  }
  
  return (
    <form className="chat-input-form" onSubmit={onFormSubmit}>
      <textarea className='chat-input-box'
        placeholder="Type your message here..."
        value={inputText}
        onChange={(e) => handleInputChange(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button type='submit' className='chat-input-button' title="Send Message">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="12" viewBox="0 0 14 12" fill="none">
          <path d="M10.2179 6.77127H0.828491L0.828491 5.22873L10.2174 5.22818L6.08013 1.09091L7.17104 0L13.171 6L7.17104 12L6.08013 10.9091L10.2179 6.77127Z" fill="white" />
        </svg>
      </button>
    </form>
  );
};

export default ChatInputComponent;