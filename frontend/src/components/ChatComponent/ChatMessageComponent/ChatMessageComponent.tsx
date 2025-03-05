import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from "remark-gfm";
import './ChatMessageComponent.css';
import { MessageSource } from '../../../enums/ChatEnums';
import { ChatMessage } from '../../../types/ChatMessageTypes';
import Plot from 'react-plotly.js';

interface ChatMessageComponentProps {
  inputMessage: ChatMessage;
  isStreaming?: boolean;
  onUpdateMessage?: (updatedMessage: ChatMessage) => void;
};

const ChatMessageComponent = ({ inputMessage, isStreaming = false, onUpdateMessage }: ChatMessageComponentProps) => {
  const [messageContent, setMessageContent] = useState(inputMessage.message);
  const plotlyData = inputMessage.plotlyJson;

  useEffect(() => {
    if (isStreaming && onUpdateMessage) {
      const interval = setInterval(() => {
        onUpdateMessage({ ...inputMessage, message: messageContent });
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [isStreaming, onUpdateMessage, inputMessage, messageContent]);

  useEffect(() => {
    setMessageContent(inputMessage.message);
  }, [inputMessage.message]);

  return (
    <div>
      {inputMessage.messageSource === MessageSource.AI && 
        <div className='ai-message-container'>
          <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60" fill="none">
            <circle cx="30" cy="30" r="29.5" fill="white" stroke="#EEEEEE" />
            <mask id="mask0_3_32" maskUnits="userSpaceOnUse" x="1" y="1" width="58" height="58">
              <circle cx="30" cy="30" r="29" fill="#D9D9D9" />
            </mask>
            <g mask="url(#mask0_3_32)">
              <path d="M47.6504 11.0376C49.0139 12.361 49.0081 14.5123 47.638 15.8424C46.8446 16.6128 45.768 16.9388 44.7377 16.8201C44.3026 16.8006 43.8722 17.0191 43.6447 17.4139C43.4431 17.7645 43.4501 18.1722 43.6265 18.5021C43.6212 18.4945 43.6159 18.4869 43.6104 18.4791C43.7036 18.6159 43.7834 18.7623 43.8478 18.9164C43.8661 18.9598 43.883 19.0043 43.8983 19.0487C43.9071 19.073 43.9146 19.0975 43.9226 19.1221C43.9377 19.1692 43.9507 19.2168 43.9627 19.2649C44.0087 19.452 44.0333 19.6472 44.0327 19.8481C44.0282 21.2151 42.8837 22.3263 41.4758 22.3302C41.3832 22.3304 41.2917 22.3257 41.2019 22.3164C40.8894 22.3169 40.5859 22.4779 40.4222 22.7622C40.2728 23.022 40.2763 23.3239 40.4033 23.5709C40.3988 23.5631 40.3945 23.555 40.3897 23.5474C40.4789 23.7024 40.5404 23.868 40.5746 24.0381C40.6822 24.578 40.5129 25.1589 40.0731 25.5683C39.3857 26.2077 38.2972 26.1881 37.6422 25.5241C36.987 24.8604 37.0132 23.8036 37.7003 23.1639C38.0069 22.8785 38.3939 22.7242 38.7863 22.6999C39.0708 22.6746 39.3378 22.5181 39.4873 22.2584C39.6507 21.9743 39.6324 21.6407 39.4687 21.3837C39.325 21.2043 39.2063 21.0054 39.1171 20.7917L39.1166 20.7912C39.0988 20.7487 39.0827 20.706 39.0676 20.6628C39.0681 20.6623 39.0681 20.6623 39.0674 20.6616C38.98 20.4108 38.9324 20.141 38.9327 19.8605C38.9372 18.4935 40.0814 17.3825 41.4893 17.3787C41.5106 17.3786 41.5318 17.379 41.5533 17.3792C41.5442 17.3793 41.5348 17.3785 41.5257 17.3786C41.9141 17.3542 42.2828 17.1443 42.4869 16.7893L42.4877 16.7885C42.4948 16.7758 42.5017 16.7632 42.5083 16.7504C42.5286 16.7116 42.5469 16.6717 42.5625 16.6316C42.5676 16.6184 42.5727 16.6046 42.5773 16.5913C42.5821 16.5778 42.5867 16.564 42.5905 16.5505C42.599 16.5237 42.6059 16.4964 42.6118 16.4691C42.6148 16.4554 42.6179 16.4416 42.6205 16.4279C42.6253 16.4006 42.6295 16.3731 42.6321 16.3455C42.6347 16.318 42.6368 16.2905 42.6376 16.2632C42.6382 16.2495 42.6384 16.236 42.6382 16.222C42.6383 16.1945 42.6371 16.1672 42.6349 16.1399C42.6337 16.1259 42.6325 16.1124 42.631 16.0992C42.6275 16.0722 42.6235 16.0452 42.6185 16.0181C42.6106 15.9779 42.6008 15.9384 42.5888 15.8991C42.5767 15.8598 42.5624 15.8213 42.5461 15.7838C42.5355 15.7587 42.5237 15.7339 42.5109 15.7097C42.5101 15.7079 42.5093 15.7067 42.5083 15.7052C42.4781 15.6478 42.4429 15.5929 42.4028 15.5412C42.4015 15.5395 42.4 15.5375 42.3987 15.5358C42.2654 15.3694 42.1505 15.1938 42.0543 15.0113C42.0314 14.9679 42.009 14.9239 41.9879 14.8793C41.9638 14.8278 41.9404 14.7755 41.919 14.7228C41.916 14.7149 41.9127 14.7073 41.9092 14.6994C41.4187 13.4809 41.6837 12.0388 42.7019 11.0503C44.0716 9.71983 46.2876 9.7144 47.6504 11.0376Z" fill="url(#paint0_linear_3_32)" />
              <path d="M49.3711 44.0505C49.3711 54.882 40.5905 44.0505 29.759 44.0505C18.9275 44.0505 10.1469 54.882 10.1469 44.0505C10.1469 33.219 18.9275 24.4384 29.759 24.4384C40.5905 24.4384 49.3711 33.219 49.3711 44.0505Z" fill="url(#paint1_linear_3_32)" />
              <path d="M10.1469 59.0394C10.1469 54.715 13.1503 50.9708 17.3718 50.0327L20.2765 49.3872C26.3355 48.0408 32.6141 48.0216 38.6812 49.331L42.1001 50.0689C46.3426 50.9846 49.3711 54.7365 49.3711 59.0767V70.1051C49.3711 80.9366 40.5905 89.7173 29.759 89.7173C18.9275 89.7173 10.1469 80.9366 10.1469 70.1051V59.0394Z" fill="url(#paint2_linear_3_32)" />
              <path fillRule="evenodd" clipRule="evenodd" d="M9.28478 53.132L9.14638 64.151C8.92245 64.5471 8.11809 65.1378 6.69217 64.3316L6.34533 72.0245C7.1688 72.5525 7.7423 73.4481 7.8196 74.4988C7.94999 76.2713 6.61882 77.8139 4.84635 77.9442C3.07387 78.0746 1.53129 76.7435 1.40089 74.971C1.30502 73.6677 1.99931 72.4888 3.0782 71.9041C2.92356 65.307 3.94694 52.4669 9.28478 53.132Z" fill="url(#paint3_linear_3_32)" />
              <path fillRule="evenodd" clipRule="evenodd" d="M50.2377 53.1578L50.407 64.1763C50.6321 64.5718 51.4381 65.1602 52.8617 64.35L53.2301 72.0411C52.4081 72.5714 51.837 73.4687 51.7627 74.5196C51.6373 76.2924 52.9727 77.8313 54.7456 77.9567C56.5184 78.0821 58.0573 76.7466 58.1827 74.9738C58.2749 73.6703 57.5774 72.4934 56.4969 71.9117C56.633 65.314 55.5735 52.4777 50.2377 53.1578Z" fill="url(#paint4_linear_3_32)" />
              <circle cx="30.0457" cy="58.9405" r="2.14732" transform="rotate(90 30.0457 58.9405)" fill="white" />
            </g>
            <defs>
              <linearGradient id="paint0_linear_3_32" x1="37.8507" y1="25.7176" x2="46.4921" y2="10.2551" gradientUnits="userSpaceOnUse">
                <stop stopColor="#EF4336" />
                <stop offset="0.19" stopColor="#EF4336" />
                <stop offset="0.24" stopColor="#FCB434" />
                <stop offset="0.39" stopColor="#FCB434" />
                <stop offset="0.54" stopColor="#EFB23B" />
                <stop offset="0.56" stopColor="#CEAD50" />
                <stop offset="0.57" stopColor="#99A471" />
                <stop offset="0.59" stopColor="#50999E" />
                <stop offset="0.61" stopColor="#048ECD" />
                <stop offset="0.81" stopColor="#048ECD" />
              </linearGradient>
              <linearGradient id="paint1_linear_3_32" x1="10.205" y1="29.3456" x2="54.7879" y2="48.715" gradientUnits="userSpaceOnUse">
                <stop stopColor="#FCD5F4" />
                <stop offset="1" stopColor="#76E2E2" />
              </linearGradient>
              <linearGradient id="paint2_linear_3_32" x1="7.03248" y1="39.8657" x2="42.5986" y2="83.9476" gradientUnits="userSpaceOnUse">
                <stop stopColor="#FCD5F4" />
                <stop offset="1" stopColor="#76E2E2" />
              </linearGradient>
              <linearGradient id="paint3_linear_3_32" x1="0.215681" y1="58.669" x2="12.9289" y2="59.0605" gradientUnits="userSpaceOnUse">
                <stop stopColor="#FCD5F4" />
                <stop offset="1" stopColor="#76E2E2" />
              </linearGradient>
              <linearGradient id="paint4_linear_3_32" x1="59.3221" y1="58.6691" x2="46.6103" y2="59.0963" gradientUnits="userSpaceOnUse">
                <stop stopColor="#FCD5F4" />
                <stop offset="1" stopColor="#76E2E2" />
              </linearGradient>
            </defs>
          </svg>
          <ReactMarkdown remarkPlugins={[remarkGfm]} className='ai-message-markdown'>
            {messageContent}
          </ReactMarkdown>
          
          {plotlyData && (
            <div className="plot-container">
              <Plot data={plotlyData.data} layout={plotlyData.layout} config={plotlyData.config || { responsive: true }} />
            </div>
          )}
        </div>
      }
      {inputMessage.messageSource === MessageSource.Human &&
       <div className='user-message-container'>
          <ReactMarkdown remarkPlugins={[remarkGfm]} className='user-message-markdown'>
            {inputMessage.message}
          </ReactMarkdown>
          <div className='svg-circle'>
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <g clipPath="url(#clip0_3_27)">
                <rect width="36" height="36" rx="18" fill="#F7FBFF" />
                <circle cx="18" cy="36" r="13" fill="#197FB3" />
                <circle cx="17.5" cy="13.5" r="7.5" fill="#197FB3" />
              </g>
              <defs>
                <clipPath id="clip0_3_27">
                  <rect width="36" height="36" rx="18" fill="white" />
                </clipPath>
              </defs>
            </svg>
          </div>
        </div>
      }
    </div>
  );
};

export default ChatMessageComponent;