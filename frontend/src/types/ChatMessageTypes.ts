import  { MessageSource } from '../enums/ChatEnums';

export interface ChatMessage {
  message: string;
  messageSource: MessageSource;
  additional_kwargs?: {
    plotly_json?: any;
  };
  plotlyJson?: any; // Add this line
}
