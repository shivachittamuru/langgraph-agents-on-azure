import React from 'react';
import './ChatShortcutComponent.css';

interface ChatShortcutComponentProps {
  shortcutText: string;
  onClick: (shortcutText: string) => void
};

const ChatShortcutComponent = ({ shortcutText, onClick }: ChatShortcutComponentProps) => {
  return (
    <button className='chat-shortcut-button' onClick={() => onClick(shortcutText)} type='button'>
      <span className='chat-shortcut-text'>
        {shortcutText}
      </span>
    </button>
  );
};

export default ChatShortcutComponent;