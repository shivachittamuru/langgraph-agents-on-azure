import axiosClient from "./api/axiosClient";
import { ChatMessage, UserInput } from '../types/ChatServiceTypes';

export const invoke_sql_agent = async (userInput: UserInput): Promise<ChatMessage> => {
  const response = await axiosClient.post<ChatMessage>('/sql-invoke', userInput);
  return response.data;
};

// export const baseURL = process.env.REACT_APP_API_URL; // adding it here for streaming

export const stream_sql_agent = async (
  message: string,
  thread_id: string,
  onMessage: (data: any) => void,
  onError: (error: any) => void
) => {
  const url = "http://localhost:8000/sql-stream";
  // const url = `${baseURL}/sql-stream`;
  const payload = {
    message: message,
    thread_id: thread_id,
    stream_tokens: true
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      onError(`Failed to get data: ${response.status}`);
      return;
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder('utf-8');
    let jsonBuffer = "";
    let foundJson = false;

    while (true) {
      const { done, value } = await reader?.read() || {};
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (!line.trim()) continue; // Ignore empty lines

        if (line.includes("plotly_json:")) {
          foundJson = true;
          jsonBuffer = line.split("plotly_json:")[1].trim(); // Corrected JSON extraction
        } else if (foundJson) {
          jsonBuffer += line.trim(); // Continue collecting JSON
        } else {
          onMessage({ content: line }); // Preserve new lines in text messages
        }
      }
    }

    if (foundJson && jsonBuffer) {
      try {
        const plotlyJson = JSON.parse(jsonBuffer); // Parse JSON correctly
        onMessage({ plotly_json: plotlyJson }); // Send Plotly data to frontend
      } catch (error: any) {
        console.error("Error parsing Plotly JSON:", error);
        onMessage({ content: `Error parsing Plotly JSON: ${error.message}` });
      }
    }
  } catch (error) {
    onError(error);
  }
};

