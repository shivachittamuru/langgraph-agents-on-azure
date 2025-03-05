export interface UserInput {
    message: string;
    thread_id?: string | null;
  }
  
  interface ToolCall {
    name: string;
    args: Record<string, any>; 
    id?: string;
    type?: "tool_call";
  }
  
  type MessageType = "human" | "ai" | "tool";
  export interface ChatMessage {
    type: MessageType;
    content: string; 
    tool_calls: ToolCall[]; 
    tool_call_id?: string; 
    run_id?: string;
    original: Record<string, any>; 
    additional_kwargs?: Record<string, any>; // Add this field for metadata like plotly JSON
  }