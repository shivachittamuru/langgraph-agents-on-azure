# 🚀 Building and Deploying Production-Grade text-to-SQL Agent(s) with LangGraph on Azure

## 📌 Overview

With the growing demand for AI-powered agents capable of interacting with databases, **Text2SQL Agents** have become essential for enterprises seeking natural language interfaces for querying structured data. Many organizations are actively exploring **single-agent and multi-agentic flows** to streamline database interactions, automate insights retrieval, and enhance user experiences.

**LangGraph**, a cutting-edge framework for building AI agents, has emerged as a preferred choice for implementing **stateful, modular, and customizable agents**. Its ability to construct **state machines** enables controlled and deterministic workflows, making it ideal for SQL query management, error handling, and conversation state retention.

This project delivers an **end-to-end production-grade implementation** of a Text2SQL Agent designed to work with the **Chinook database** (a sample database representing a digital music store). The solution covers **design, development, and deployment** phases, ensuring best practices for **reliability, security, and scalability** when deploying on **Azure**.

## 🎯 Key Features & Objectives

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

### ✅ Chat UI with React
- Developed a **React-based chat interface** for user interaction.

### ✅ Cloud-Native Deployment
- **Containerized** both the **Chat UI** and **Agent APIs** using Docker.
- Prepared for **Azure deployment** on **Azure Web App** or **Azure Kubernetes Service (AKS)**.


## ⚡ Getting Started

Clone the repo:
```console
git clone https://github.com/shivachittamuru/langgraph-agents-on-azure.git
cd langgraph-agents-on-azure
```

Create a conda environment:
```console
conda create --name <env-name> python=3.10
conda activate <env-name>
```

Install `PIP` requirements
```console
pip install -r requirements.txt
```

Update the values in `.env-sample` and rename it to `.env`.

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
