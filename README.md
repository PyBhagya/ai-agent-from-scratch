# AI Agent From Scratch 🚀

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/LangChain-Powered-green.svg" alt="LangChain Powered">
  <img src="https://img.shields.io/badge/Gemini-AI-red.svg" alt="Gemini AI">
  <img src="https://img.shields.io/badge/Streamlit-UI-orange.svg" alt="Streamlit UI">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</div>

This repository documents my learning journey of creating an AI agent in Python, based on [TechWithTim's YouTube tutorial](https://www.youtube.com/@TechWithTim). It walks through building a research assistant that uses Google's Gemini AI model, along with external tools like Wikipedia Search and DuckDuckGo. The project includes both a command-line interface and a Streamlit web application.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Usage Examples](#-usage-examples)
- [How It Works](#-how-it-works)
- [References](#-references)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠 Features

- **LLM Integration**: Seamless usage of Google's Gemini 1.5 Pro model via LangChain
- **Tool Integrations**:
  - Wikipedia API for encyclopedia knowledge
  - DuckDuckGo Search for real-time web results
  - Custom tools (e.g., save output to file, text processing)
- **Structured Outputs**: Clean, formatted responses using Pydantic models
- **Error Handling**: Robust error management and graceful failure modes
- **Extensible Architecture**: Easy to add new tools and capabilities
- **Development Environment**: Complete setup with virtual environment and dependency management
- **Web Interface**: Interactive Streamlit web application for easy usage

## 📂 Project Structure

```bash
/ai-agent-from-scratch
|
├── main.py          # Command-line interface for the AI Agent
├── app.py           # Streamlit web application interface
├── tools.py         # Definitions of custom and external tools
├── .env             # Environment variables for API keys
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## 📊 Requirements

- Python 3.10+
- Visual Studio Code (recommended)
- API Keys:
  - Google Gemini API key for the Gemini 1.5 Pro model

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-agent-from-scratch.git
   cd ai-agent-from-scratch
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Mac/Linux
   python3 -m venv venv
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   # On Windows
   pip install -r requirements.txt

   # On Mac/Linux
   pip3 install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with your API key:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

## ⚙️ How to Run

1. **Ensure your virtual environment is activated**:
   ```bash
   # On Mac/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

2. **Run the command-line interface**:
   ```bash
   # On Windows
   python main.py

   # On Mac/Linux
   python3 main.py 
   ```

   OR

   **Run the web application**:
   ```bash
   streamlit run app.py
   ```

3. **Interact with the agent** by typing your research questions or tasks in either interface.

## 💡 Usage Examples

Here are some example queries you can try with the agent:

- "What are the key differences between transformer and RNN architectures?"
- "Find information about climate change impacts and summarize the findings."
- "Research the history of artificial intelligence and save the results to a file."

## 🔍 How It Works

This AI agent uses a combination of:

1. **LangChain Framework**: For orchestrating the agent's behavior and tool usage
2. **Google Gemini 1.5 Pro**: For understanding queries and generating responses
3. **External Tools**: For retrieving information from various sources
4. **Prompt Engineering**: For guiding the model to produce useful outputs
5. **Streamlit**: For creating an interactive web interface

The agent follows this workflow:
1. Parse user input
2. Determine which tools to use
3. Execute tools to gather information
4. Synthesize results into a coherent response
5. Present the answer to the user

## 📚 References

- [TechWithTim YouTube Channel](https://www.youtube.com/@TechWithTim)
- [LangChain Documentation](https://docs.langchain.dev/)
- [Google Gemini API Documentation](https://ai.google.dev/docs/gemini_api_overview)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🌟 Future Improvements

- Add more tools:
  - YouTube Search
  - Arxiv Search for academic papers
  - Google Scholar integration
- Enable file upload and processing
- Implement multi-turn conversations with memory
- Add a web interface for easier interaction
- Implement caching for faster responses
- Add unit tests and CI/CD pipeline

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p>Built with ❤️ by <a href="https://github.com/PyBhagya">PyBhagya</a></p>
</div>

