

# 🤖 Multi-Agent Research & Chart Generation System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Workflow-green)
![LangChain](https://img.shields.io/badge/LangChain-AI%20Framework-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-API-black)
![License](https://img.shields.io/badge/License-MIT-yellow)

A **LangGraph powered multi-agent system** where specialized AI agents collaborate to research information and generate data visualizations automatically.

This project demonstrates how **multiple AI agents can work together in a workflow** to complete complex tasks like:

* Data research
* Data processing
* Chart generation

---

# 🚀 Features

### 🔍 Research Agent

* Collects information from the internet
* Uses **search APIs** to gather relevant data
* Extracts structured information
* Sends results to other agents

### 📊 Chart Generator Agent

* Receives data from Research Agent
* Uses **Python tools** to create charts
* Generates visual insights from raw data

### 🤝 Multi-Agent Collaboration

* Agents communicate through **LangGraph workflow**
* Each agent performs a **specialized task**
* Data flows automatically between agents

---

# 🏗️ System Architecture

```
                ┌───────────────┐
                │      User      │
                │   Ask Query    │
                └───────┬────────┘
                        │
                        ▼
             ┌────────────────────┐
             │   Research Agent    │
             │  (Web Data Fetch)   │
             └─────────┬───────────┘
                       │
                       ▼
             ┌────────────────────┐
             │ Chart Generator    │
             │   (Python Tool)    │
             └─────────┬──────────┘
                       │
                       ▼
                ┌───────────────┐
                │   Final Output │
                │  Charts + Data │
                └───────────────┘
```

---

# 🧠 Workflow

1️⃣ User asks a research question

Example:

```
Show population growth of India for the last 20 years.
```

2️⃣ **Research Agent**

* Searches the web
* Collects relevant data

3️⃣ **Chart Generator Agent**

* Receives structured data
* Generates charts using Python

4️⃣ System returns:

* research insights
* generated chart

---

# 🛠️ Tech Stack

| Technology                | Purpose                   |
| ------------------------- | ------------------------- |
| Python                    | Core programming language |
| LangChain                 | LLM framework             |
| LangGraph                 | Multi-agent orchestration |
| OpenAI API                | LLM intelligence          |
| Tavily API                | Web search                |
| Matplotlib / Python Tools | Chart generation          |

---

# 📦 Installation

Clone repository

```bash
git clone https://github.com/yourusername/multi-agent-research-chart-system.git
cd multi-agent-research-chart-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env` file

```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Optional (LangSmith tracing)

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=multi-agent-research
```

---

# ▶️ Run the Project

```
python main.py
```

Example query:

```
Compare GDP growth of India and China and create a chart.
```

Output:

* researched data
* generated chart visualization

---

# 📂 Project Structure

```
multi-agent-project/
│
├── main.py
│
├── agents/
│   ├── researcher_agent.py
│   ├── chart_agent.py
│
├── tools/
│   ├── search_tool.py
│   ├── chart_tool.py
│
├── requirements.txt
└── README.md
```

---

# 📊 Multi-Agent Flow (LangGraph)

```
User Query
     │
     ▼
Research Agent
     │
     ▼
Data Processing
     │
     ▼
Chart Agent
     │
     ▼
Final Visualization
```

---

# 🏆 Key Benefits

✔ Demonstrates **real-world multi-agent architecture**
✔ Modular agent design
✔ Easy to extend with new agents
✔ Clear LangGraph workflow orchestration

---

# 🔮 Future Improvements

* 📈 Data Analysis Agent
* 📑 Report Generator Agent
* 🌐 Web UI Dashboard
* 🗄️ Database storage
* 🤖 More specialized agents

---

# 📜 License

MIT License

---

अगर चाहो तो मैं तुम्हारे project के लिए और भी powerful चीजें बना सकता हूँ:

* **🔥 GitHub project banner image**
* **LangGraph workflow diagram (professional)**
* **agent architecture diagram**
* **portfolio-level README (जो recruiters को impress करे)**

अगर बोलो तो मैं **5 मिनट में README को GitHub trending level बना दूंगा** 🚀
