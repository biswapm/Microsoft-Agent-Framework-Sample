# Research Agent with Blog Post Generation

A comprehensive agent framework implementation using Microsoft Agent Framework with both Azure AI Foundry Agent and Azure OpenAI Chat Completion Agent, featuring research capabilities and blog post generation with orchestration.

## Prerequisites

1. Azure AI Foundry project set up
2. Azure OpenAI service with chat completion deployment
3. Azure CLI installed and authenticated (`az login`)
4. Python 3.8+ installed

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your Azure settings:
   ```bash
   cp .env.example .env
   ```
4. Update the `.env` file with your configuration:
   - **Azure AI Foundry settings:**
     - `AZURE_AI_PROJECT_ENDPOINT`: Your Azure AI project endpoint
     - `AZURE_AI_MODEL_DEPLOYMENT_NAME`: Your model deployment name (e.g., gpt-4o-mini)
   - **Azure OpenAI settings:**
     - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint
     - `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`: Your chat deployment name (e.g., gpt-4o-mini)

## Quick Start

1. **Setup (recommended)**:
   ```bash
   python setup.py
   ```

2. **Manual setup**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Azure AI settings
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Test your configuration**:
   ```bash
   # Test basic research agent configuration
   python test_config.py
   
   # Test full orchestration configuration (research + blog)
   python test_orchestration_config.py
   ```

## Running Individual Components

### Research Agents
```bash
# Basic research agent
python src/basic_researcher.py

# Interactive research session
python src/interactive_researcher.py

# Advanced research with custom tools
python src/researcher_with_tools.py
```

### Blog Post Generation
```bash
# Blog post agent (Azure OpenAI)
python src/blog_post_agent.py

# Complete research-to-blog orchestration
python src/research_blog_orchestrator.py
```

## Project Structure

```
Microsoft-Agent-Framework-Sample/
├── src/
│   ├── __init__.py
│   ├── basic_researcher.py          # Simple research agent (AI Foundry)
│   ├── interactive_researcher.py    # Conversational research agent (AI Foundry)
│   ├── researcher_with_tools.py     # Advanced agent with custom tools (AI Foundry)
│   ├── blog_post_agent.py          # Blog writing agent (Azure OpenAI)
│   ├── research_blog_orchestrator.py # Sequential orchestration workflow
│   └── utils.py                     # Shared utilities and configuration
├── main.py                          # Main entry point with menu
├── setup.py                         # Setup and configuration script
├── test_config.py                   # AI Foundry configuration test
├── test_orchestration_config.py     # Full orchestration configuration test
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore file
├── LICENSE                          # MIT License
└── README.md                        # This file
```

## Features

### Research Capabilities
- **Basic Research**: Simple question-answering research agent
- **Interactive Mode**: Continuous conversation for follow-up questions
- **Custom Tools**: Research agent with academic search, statistics, and timeline tools
- **Streaming Responses**: Real-time response streaming

### Blog Post Generation
- **Blog Writing**: Transform research into engaging blog posts
- **Multiple Styles**: Professional, casual, and technical writing styles
- **Content Refinement**: Iterative improvement based on feedback
- **Outline Creation**: Generate structured blog post outlines

### Orchestration
- **Sequential Workflow**: Research-to-blog pipeline using multiple agents
- **Azure AI Foundry + OpenAI**: Combines specialized agents for optimal results
- **End-to-End**: Complete content creation from topic to published blog post
- **Clean Architecture**: Modular and extensible design

## Configuration

The agents can be configured through environment variables or directly in code:

- **Research Agents**: Use Azure AI Foundry Agent for comprehensive research capabilities
- **Blog Post Agent**: Uses Azure OpenAI Chat Completion for creative content generation  
- **Orchestration**: Combines both services in a sequential workflow

See the examples in the `src/` directory for different configuration approaches and the `.env.example` file for all available settings.

## License

MIT License - see LICENSE file for details.