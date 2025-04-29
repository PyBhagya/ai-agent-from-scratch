# AI Agent From Scratch 🚀

This repository documents my learning journey of creating an AI agent in Python, based on [TechWithTim's YouTube tutorial](https://www.youtube.com/@TechWithTim).  
It walks through building a research assistant that uses Large Language Models (LLMs) like OpenAI's GPT and Anthropic's Claude, along with external tools like Wikipedia Search and DuckDuckGo.

---

## 🛠 Features

- Setup of virtual environment and project structure
- Usage of LLMs (GPT, Claude) via LangChain
- Tool integrations:
  - Wikipedia API
  - DuckDuckGo Search
  - Custom tools (e.g., save output to file)
- Structured and formatted outputs using Pydantic models
- Error handling and robustness

---

## 📂 Project Structure

```bash
/ai-agent-from-scratch
|
|├— main.py          # Main logic for running the AI Agent
|├— tools.py         # Definitions of custom and external tools
|├— .env             # Environment variables for API keys
|└— requirements.txt # Project dependencies
```

---

## 📊 Requirements

- Python 3.10+
- Visual Studio Code (recommended)
- API Keys (OpenAI or Anthropic Claude)

Install dependencies:
```bash
pip install -r requirements.txt
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows
```

---

## ⚙️ How to Run

1. Add your API keys in `.env` file:
   ```text
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```
2. Run the project:
   ```bash
   python main.py
   ```

---

## 📚 References

- [TechWithTim YouTube Channel](https://www.youtube.com/@TechWithTim)
- [LangChain Documentation](https://docs.langchain.dev/)

---

## 🌟 Future Improvements

- Add more tools like YouTube Search, Arxiv Search.
- Enable file upload and multiple queries.
- Explore agent memory (saving chat history).

---

git config --global user.email "you@example.com"
  git config --global user.name "Your Name"