# Microsoft Agent Framework Sample - Research & Blog Orchestrator

A comprehensive implementation of Microsoft Agent Framework featuring interactive research agents, AI-powered blog generation, and sequential orchestration workflows. This sample demonstrates how to build production-ready AI agents using Azure AI Foundry and Azure OpenAI services with an integrated DevUI for testing and interaction.

![DevUI Screenshot](https://github.com/biswapm/Microsoft-Agent-Framework-Sample/blob/main/docs/devui-screenshot.png)

## 🚀 Features

### 🔬 **Research Agents**
- **Interactive Research Agent**: Conversational research with context retention using Azure AI Foundry
- **Advanced Research Tools**: Custom tools for academic search, statistics, and timeline analysis
- **Streaming Responses**: Real-time response streaming for better user experience

### 📝 **Blog Generation**
- **LangChain Blog Agent**: Advanced blog writing using LangChain with Azure OpenAI
- **Multiple Writing Styles**: Professional, casual, technical, and SEO-optimized content
- **Content Formatting**: Automatic markdown formatting with proper structure

### 🎯 **Orchestration**
- **Sequential Workflow**: Research-to-blog pipeline combining multiple specialized agents
- **End-to-End Pipeline**: Complete content creation from research topic to published blog post
- **Error Handling**: Robust error handling and graceful degradation

### 🖥️ **DevUI Integration**
- **Interactive Web Interface**: Built-in DevUI for testing and interacting with agents
- **OpenTelemetry Tracing**: Full observability and debugging capabilities
- **Real-time Testing**: Live agent testing at `http://localhost:8082`

## 📋 Prerequisites

1. **Azure AI Foundry project** set up with model deployment
2. **Azure OpenAI service** with chat completion deployment  
3. **Azure CLI** installed and authenticated (`az login`)
4. **Python 3.8+** installed

## ⚡ Quick Start

### 1. **Clone & Setup Environment**
```bash
git clone https://github.com/biswapm/Microsoft-Agent-Framework-Sample.git
cd Microsoft-Agent-Framework-Sample

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configure Azure Services**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure settings
# - AZURE_AI_PROJECT_ENDPOINT: Your Azure AI Foundry project endpoint
# - AZURE_AI_MODEL_DEPLOYMENT_NAME: Your model deployment (e.g., gpt-4o)
# - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
# - AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: Your chat deployment name
```

### 3. **Run the Application**
```bash
# Start DevUI with all agents
python main.py

# Access the web interface
# Open browser to: http://localhost:8082
```

## 🧪 Testing Your Agents

### **Research Agent Test Prompts**
```
Analyze the current state of large language models in 2025. What are the key developments in efficiency, multimodality, and reasoning capabilities?

Research the impact of quantum computing on cryptography. What are the timeline and implications for current security systems?

Investigate the latest developments in autonomous vehicle technology. What are the main technical challenges and regulatory hurdles?
```

### **Blog Orchestrator Test Prompts**
```
Create a comprehensive blog post about the future of AI coding assistants and their impact on software development

Write a blog post explaining edge computing for business leaders - what it is, why it matters, and how to implement it

Create a blog post about building effective remote teams in the hybrid work era, including tools and strategies
```

## 🏗️ Project Architecture

```
Microsoft-Agent-Framework-Sample/
├── src/
│   ├── interactive_researcher.py    # Azure AI Foundry research agent
│   ├── langchain_blog_agent.py     # LangChain blog writing agent  
│   ├── research_blog_orchestrator.py # Sequential workflow orchestrator
│   ├── researcher_with_tools.py     # Advanced research with custom tools
│   ├── devui_config.py             # DevUI configuration
│   └── utils.py                     # Shared utilities
├── agents/                          # Agent package modules
│   ├── interactive_researcher/
│   └── research_blog_orchestrator/
├── main.py                          # DevUI entry point with all agents
├── devui_launcher.py               # Alternative DevUI launcher
├── setup_agents.py                 # Agent setup and configuration
├── requirements.txt                # Dependencies including agent-framework
├── .env.example                    # Environment template
├── .gitignore                      # Comprehensive gitignore for AI projects
└── README.md                       # This documentation
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Azure AI Foundry (for Research Agent)
AZURE_AI_PROJECT_ENDPOINT="https://your-project.services.ai.azure.com/api/projects/YourProject"
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o

# Azure OpenAI (for Blog Agent)  
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
OPENAI_API_VERSION=2024-02-01

# Optional: Agent-specific settings
# AZURE_AI_AGENT_ID=asst_your_agent_id  # Use existing agent
# AZURE_OPENAI_API_KEY=your_key         # If not using Azure CLI auth
```

### **Agent Capabilities**

| Agent | Service | Capabilities |
|-------|---------|-------------|
| **Research Agent** | Azure AI Foundry | Interactive research, context retention, conversational follow-ups |
| **Blog Agent** | Azure OpenAI + LangChain | Content creation, formatting, SEO optimization, multiple styles |
| **Orchestrator** | Sequential Workflow | Research-to-blog pipeline, error handling, result aggregation |

## 🚀 Running Individual Components

### **Research Agents**
```bash
# Interactive research session
python src/interactive_researcher.py

# Advanced research with custom tools  
python src/researcher_with_tools.py
```

### **Blog Generation** 
```bash
# Standalone blog generation
python src/langchain_blog_agent.py

# Complete research-to-blog workflow
python src/research_blog_orchestrator.py
```

### **DevUI Testing**
```bash
# Launch DevUI with all agents
python main.py

# Alternative launcher
python devui_launcher.py
```

## 🔍 Observability & Debugging

- **OpenTelemetry Tracing**: Enabled by default when running DevUI
- **Agent Logs**: Available in the DevUI interface
- **Error Handling**: Comprehensive error messages with troubleshooting guidance
- **Health Checks**: Built-in health monitoring for all services

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📚 Resources

- [Microsoft Agent Framework Documentation](https://microsoft.github.io/agent-framework/)
- [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-foundry/)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
- [LangChain Documentation](https://python.langchain.com/)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Microsoft Agent Framework, Azure AI, and LangChain**