# 🚀 Build and Deploy Production-Grade LangGraph Agent(s) on Azure

## 📌 Overview

With the growing demand for AI-powered agents capable of interacting with databases, **Text2SQL Agents** have become essential for enterprises seeking natural language interfaces for querying structured data. Many organizations are actively exploring **single-agent and multi-agentic flows** to streamline database interactions, automate insights retrieval, and enhance user experiences.

**LangGraph**, a cutting-edge framework for building AI agents, has emerged as a preferred choice for implementing **stateful, modular, and customizable agents**. Its ability to construct **state machines** enables controlled and deterministic workflows, making it ideal for SQL query management, error handling, and conversation state retention.

This project delivers an **end-to-end production-grade implementation** of a Text2SQL Agent designed to work with the **Chinook database** (a sample database representing a digital music store). The solution covers **design, development, and deployment** phases, ensuring best practices for **reliability, security, and scalability** when deploying on **Azure**.

## 🎯 Key Features

### ✅ SQL Agent Development
- Built a **custom SQLAgent class** from scratch using the **Chinook SQLite database**.
- Implemented **asynchronous execution** for non-blocking performance.
- Developed **FastAPI-based APIs** with `invoke` and `stream` endpoints.

### ✅ Conversation State Management
- Integrated **SQLite checkpointers** to persistently store conversations.
- Approaches to filter conversation state:
  - **Rolling Window Strategy**: Retain only the last *N* conversation turns for relevance.
  - **Summary Strategy**: Maintain a **running summary** with weighted emphasis on recent interactions.
  - **Hybrid Strategy**: Combine rolling window + summary for deeper context preservation.

### ✅ Streaming Responses
- Enabled **real-time streaming** of generated responses for a seamless user experience.

### ✅ Observability and Tracing
- Implemented **Azure AI Foundry tracing** to monitor and log agent execution.
- Captured **agent runs, request-response cycles, and error diagnostics** for debugging and analytics.

> **Note:** If you are new to the LangGraph framework, navigate to `backend\notebooks` and execute the 5 notebooks in order to see the above key features in action.

### ✅ Chat UI with React
- Developed a **React-based chat interface** for user interaction.

### ✅ Cloud-Native Deployment
- **Containerized** both the **Chat UI** and **Agent APIs** using Docker.
- Prepared for **Azure deployment** on **Azure Web App** or **Azure Kubernetes Service (AKS)**.


## ⚡ Setup Development Environment

You can use GitHub Codespaces where we have a pre-configured development environment set up and ready to go for you, or you can setup the developer tools on your local workstation.

- [Use GitHub Codespaces](#use-github-codespaces)
- [Use Local Workstation](#use-local-workstation)

### Use Github Codespaces

If you want to setup your environment on your local workstation, expand the section below and follow the requirements listed.

<details markdown=1>
<summary markdown="span">Click to expand/collapse GitHub Codespaces Requirements</summary>

You must have a GitHub account to use GitHub Codespaces. If you do not have a GitHub account, you can [Sign Up Here](https://github.com/signup).

GitHub Codespaces is available for developers in every organization. All personal GitHub.com accounts include a monthly quota of free usage each month. GitHub will provide users in the Free plan 120 core hours, or 60 hours of run time on a 2 core codespace, plus 15 GB of storage each month.

You can see your balance of available codespace hours on the [GitHub billing page](https://github.com/settings/billing/summary).

Your Codespace environment should load in a new browser tab. It will take approximately 3-5 minutes the first time you create the codespace for it to load.

- When the codespace completes loading, you should find an instance of Visual Studio Code running in your browser with the files needed for this project. 
- Python modules required to run the `/backend` code are pre-installed with the codespace, so you can start coding immediately without the need to set up an environment. This is one of the key benefits of using GitHub Codespaces.

**NOTE:** GitHub Codespaces time out after 20 minutes if you are not actively interacting with it in the browser. If your codespace times out, you can restart it and the developer environment and its files will return with its state intact within seconds. If you want to have a better experience, you can also update the default timeout value in your personal setting page on Github. Refer to this page for instructions: [Default-Timeout-Period](https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces#setting-your-default-timeout-period) 

**NOTE:** Codespaces expire after 30 days unless you extend the expiration date. When a Codespace expires, the state of all files in it will be lost.

### Use Local Workstation

If you want to setup your environment on your local workstation, expand the section below and follow the requirements listed.

<details markdown=1>
<summary markdown="span">Click to expand/collapse Local Workstation Requirements</summary>

Clone the repo:
```console
git clone https://github.com/shivachittamuru/langgraph-agents-on-azure.git
cd langgraph-agents-on-azure
```

#### Option 1: Using Conda (Recommended)
If you have Anaconda or Miniconda installed, you can set up the environment using Conda:
```console
conda create --name <env-name> python=3.10
conda activate <env-name>
pip install -r requirements.txt
```

#### Option 2: Using Virtualenv
```console
python3 -m venv <env-name>
source <env-name>/bin/activate  # On macOS/Linux
<env-name>\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 🚀 Run the Application

#### 1️⃣ Configure Environment Variables  
- Open `.env-sample` in both backend and frontend, update the environment variables with your **Azure configuration**, and rename it to `.env`.  

#### 2️⃣ Start the Backend Agent API  
Run the following commands in your terminal:  
```console
cd backend
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) to view it in your browser, and [http://localhost:8000/docs](http://localhost:8000/docs) to view and test the APIs.  

Use the [test_agent_api.ipynb](test_agent_api.ipynb) notebook to test the APIs with various questions. Feel free to tweak the code and observe the changes to evaluate the agent's accuracy and consistency.

#### 3️⃣ Start the Frontend React UI
3. Run the following commands in your terminal:
```console
cd frontend
npm install  # Install dependencies (only needed once)
npm start    # Start the frontend server
```

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.


## 📝 Agent Test Questions  

1. *Can you tell me the names of popular albums in the database?*  
2. *Find albums released by artists who have more than 5 albums.*  
3. *Who are the top 5 employees who have made the most sales?*  
4. *Can you list the top 5 most expensive tracks?*  
5. *Which album has the most tracks?*  



## 🛠️ Future Enhancements
- 🔹 Implement new agents such as a Visualization Agent to create plots for numeric analysis.
- 🔹 Build and deploy **multi-agentic flows**.
- 🔹 Expand to support **multiple database backends**.
- 🔹 Use Postgres as checkpointer database for storing conversation state.
- 🔹 Ensure security and Trustworthy AI principles are sufficiently added.


## Contributors

- Alexis Joseph
- Caroline Matthews
- Daniel Kondrashevich
- Shiva Chittamuru
