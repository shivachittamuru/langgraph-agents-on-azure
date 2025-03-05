import axios from 'axios';

const axiosClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // responseType: 'stream', 
  // axios is not designed for streaming responses. 
  // Use fetch API or another library that is designed for streaming, such as node-fetch or got.
});

export default axiosClient;

