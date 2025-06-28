# 📝 Hermes – Stateful To‑Do Agent

A conversational to-do list manager powered by the OpenAI Agents SDK with Gemini LLM, wrapped in a sleek Chainlit chat UI. Hermes remembers your to-dos during each session and lets you **add**, **remove**, **list**, and **prioritize** tasks effortlessly.

---

## 🚀 Table of Contents

1. [About the Project](#about-the-project)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Prerequisites](#prerequisites)  
5. [Quick Start](#quick-start)  
6. [Usage Examples](#usage-examples)  
7. [Project Structure](#project-structure)  
8. [Roadmap](#roadmap)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## 📌 About the Project

Hermes is built to make productivity conversational and intuitive. Instead of complex UIs or buried settings, you just chat:

- **Add tasks**: “Add buy groceries”  
- **List tasks**: “Show me my to-dos”  
- **Remove tasks**: “Remove task 2”  

Everything runs in a smooth chat interface, and all list updates are handled through a tool-driven agent system—enforcing structure and reducing mistakes.

---

## ✨ Features

- **Session-based memory** – Remembers tasks throughout the chat.  
- **Gemini LLM agent** – Powered by `OpenAIChatCompletionsModel`.  
- **Tool-first actions** – Uses a `todo_manager_tool` for all list manipulations.  
- **Chainlit chat UI** – Clean, interactive, and intuitive.

---

## 🧰 Tech Stack

- **Python** – Core development  
- **Chainlit** – Conversational interface  
- **OpenAI Agents SDK** – Agent orchestration  
- **Gemini LLM** – Task reasoning backend  
- **dotenv** – Environment variable management  

---

## 📋 Prerequisites

Ensure you have:

- Python 3.10+  
- `pip install openai-agents chainlit openai python-dotenv`

---

## ⚙️ Quick Start

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your_username/hermes-todo-agent.git
   cd hermes-todo-agent
