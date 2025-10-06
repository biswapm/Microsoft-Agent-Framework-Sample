"""
DevUI with Working Researcher and Blog Agents
Simplified version focused on getting both agents working prop            async def run_stream(self, query: str, thread=None, **kwargs):
                \"\"\"Stream method for DevUI compatibility.\"\"\"
                try:
                    result = await self.run(query)
                    # Yield the result as a stream
                    yield result
                except Exception as e:
                    yield f\"Error: {e}\"y.
"""

import asyncio
import os
from dotenv import load_dotenv

# Enable OpenTelemetry tracing for DevUI
os.environ["ENABLE_OTEL"] = "true"

# Add Azure CLI to PATH if not already there
azure_cli_path = "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin"
if azure_cli_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] += f";{azure_cli_path}"


def create_working_agents():
    """Create working versions of both agents for DevUI."""
    
    load_dotenv()
    agents = []
    
    print("Creating working agents...")
    
    # 1. Create Working Blog Agent
    try:
        from src.langchain_blog_agent import LangChainBlogAgent
        print("   Loading LangChain Blog Agent...")
        
        blog_agent = LangChainBlogAgent()
        blog_agent.initialize()
        
        # Create a proper wrapper for DevUI
        class BlogAgentForDevUI:
            def __init__(self, blog_agent):
                self.blog_agent = blog_agent
                self.name = "Blog Writer Agent"
                self.description = "AI blog writer using LangChain with formatting and SEO tools"
            
            async def run(self, query, **kwargs):
                """Run the blog agent with a query."""
                try:
                    # Extract text content from ChatMessage if needed
                    if hasattr(query, 'content'):
                        query_text = query.content
                    elif hasattr(query, 'text'):
                        query_text = query.text
                    elif isinstance(query, str):
                        query_text = query
                    else:
                        query_text = str(query)
                    
                    response = await self.blog_agent.run(query_text)
                    
                    # Extract content from BlogResult object
                    if hasattr(response, 'text'):
                        result = response.text
                    elif hasattr(response, 'content'):
                        result = response.content
                    elif hasattr(response, 'output'):
                        result = response.output
                    else:
                        result = str(response)
                    
                    # Ensure we return the full content
                    return result
                except Exception as e:
                    return f"Blog generation error: {e}"
            
            async def run_stream(self, query: str, thread=None, **kwargs):
                """Stream method for DevUI compatibility."""
                try:
                    result = await self.run(query)
                    # Yield the result as a stream
                    yield result
                except Exception as e:
                    yield f"Error: {e}"
        
        wrapped_blog = BlogAgentForDevUI(blog_agent)
        agents.append(wrapped_blog)
        print("   Blog Agent loaded successfully")
        
    except Exception as e:
        print(f"   Failed to load Blog Agent: {e}")
    
    # 2. Create Working Researcher Agent with real Azure AI
    try:
        print("   Loading Researcher Agent...")
        from src.interactive_researcher import InteractiveResearcher
        
        class ResearcherAgentForDevUI:
            def __init__(self):
                self.name = "Research Agent"
                self.description = "AI research assistant powered by Azure AI Foundry"
                self.researcher = InteractiveResearcher()
                self._initialized = False
            
            async def _ensure_initialized(self):
                """Ensure the researcher is initialized."""
                if not self._initialized:
                    await self.researcher.initialize()
                    self._initialized = True
            
            async def run(self, query, **kwargs):
                """Run research on the given query using Azure AI."""
                try:
                    # Extract text content from ChatMessage if needed
                    if hasattr(query, 'content'):
                        query_text = query.content
                    elif hasattr(query, 'text'):
                        query_text = query.text
                    elif isinstance(query, str):
                        query_text = query
                    else:
                        query_text = str(query)
                    
                    # Initialize if needed
                    await self._ensure_initialized()
                    
                    # Use the real Azure AI research agent
                    research_result = await self.researcher.research(query_text)
                    return research_result
                    
                except Exception as e:
                    error_msg = f"Azure AI Research error: {e}"
                    print(f"   ⚠️ {error_msg}")
                    return f"""# Research Error

Unable to connect to Azure AI services for research.

**Error Details:** {e}

**Troubleshooting:**
1. Ensure Azure CLI is authenticated (`az login`)
2. Check your .env file has valid Azure AI settings
3. Verify your Azure AI project and model deployment
4. Check your internet connection

**Environment Variables Required:**
- AZURE_AI_PROJECT_ENDPOINT
- AZURE_AI_MODEL_DEPLOYMENT_NAME

Please resolve these issues and try again."""
            
            async def run_stream(self, query, thread=None, **kwargs):
                """Stream method for DevUI compatibility."""
                try:
                    result = await self.run(query)
                    # Yield the result as a stream
                    yield result
                except Exception as e:
                    yield f"Error: {e}"
        
        researcher = ResearcherAgentForDevUI()
        agents.append(researcher)
        print("   Researcher Agent loaded successfully")
        
    except Exception as e:
        print(f"   Failed to load Researcher Agent: {e}")
    
    # 3. Create Working Orchestrator Agent
    try:
        print("  Loading Orchestrator Agent...")
        from src.research_blog_orchestrator import ResearchToBlogOrchestrator
        
        class OrchestratorAgentForDevUI:
            def __init__(self):
                self.name = "Research-to-Blog Orchestrator"
                self.description = "Orchestrates research and blog creation in a sequential workflow"
                self.orchestrator = ResearchToBlogOrchestrator()
                self._initialized = False
            
            async def _ensure_initialized(self):
                """Ensure the orchestrator is initialized."""
                if not self._initialized:
                    await self.orchestrator.initialize()
                    self._initialized = True
            
            async def run(self, query, **kwargs):
                """Run the orchestrator with a query to create research + blog."""
                try:
                    # Extract text content from ChatMessage if needed
                    if hasattr(query, 'content'):
                        query_text = query.content
                    elif hasattr(query, 'text'):
                        query_text = query.text
                    elif isinstance(query, str):
                        query_text = query
                    else:
                        query_text = str(query)
                    
                    # Initialize if needed
                    await self._ensure_initialized()
                    
                    # Use the orchestrator to create research + blog
                    workflow_results = await self.orchestrator.create_blog_from_topic(query_text)
                    
                    # Format the combined result
                    research_content = workflow_results.get("research", {}).get("content", "No research generated")
                    blog_content = workflow_results.get("blog_post", {}).get("content", "No blog generated")
                    
                    combined_result = f"""# Research-to-Blog Workflow Results

## 📊 Research Phase
{research_content}

---

## 📝 Blog Post Phase  
{blog_content}

---
*Workflow completed successfully via Sequential Research-to-Blog Orchestrator*"""
                    
                    return combined_result
                    
                except Exception as e:
                    error_msg = f"Orchestrator workflow error: {e}"
                    print(f"   {error_msg}")
                    return f"""# Orchestrator Workflow Error

Unable to complete the research-to-blog workflow.

**Error Details:** {e}

**Troubleshooting:**
1. Ensure both research and blog agents are properly configured
2. Check Azure AI and LangChain authentication
3. Verify all required environment variables are set

The orchestrator combines research and blog creation in a sequential workflow."""
            
            async def run_stream(self, query, thread=None, **kwargs):
                """Stream method for DevUI compatibility."""
                try:
                    result = await self.run(query)
                    # Yield the result as a stream
                    yield result
                except Exception as e:
                    yield f"Error: {e}"
        
        orchestrator = OrchestratorAgentForDevUI()
        agents.append(orchestrator)
        print("    Orchestrator Agent loaded successfully")
        
    except Exception as e:
        print(f"   Failed to load Orchestrator Agent: {e}")
    
    return agents


def main():
    """Launch DevUI with working agents and tracing enabled."""
    
    print("Starting DevUI with Working Agents...")
    print("=" * 50)
    
    # Ensure tracing environment is set
    print("Configuring tracing...")
    os.environ["ENABLE_OTEL"] = "true"
    print("    ENABLE_OTEL=true set")
    
    # Check if DevUI is available
    try:
        from agent_framework.devui import serve
        print("Agent Framework DevUI is available")
    except ImportError:
        try:
            from agent_framework_devui import serve
            print("Agent Framework DevUI is available (legacy import)")
        except ImportError:
            print("Agent Framework DevUI not found")
            print("Please install: pip install agent-framework-devui")
            return
    
    try:
        # Create working agents
        agents = create_working_agents()
        
        if agents:
            print(f"\\n Successfully created {len(agents)} working agent(s)!")
            print(" Starting DevUI with tracing enabled...")
            print(" Access URL: http://localhost:8082")
            print(" Tracing: ENABLED (OTEL)")
            print("Press Ctrl+C to stop")
            print()
            
            # Start DevUI with working agents (tracing enabled via environment variable)
            serve(entities=agents, auto_open=True, port=8082)
            
        else:
            print("\\nNo agents could be created. Starting with sample gallery...")
            serve(entities=[], auto_open=True, port=8082)
        
    except Exception as e:
        print(f" DevUI failed to start: {e}")
        print("\\nTroubleshooting:")
        print("1. Check if port 8082 is available")
        print("2. Verify agent-framework-devui is installed")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\nGoodbye!")
    except Exception as e:
        print(f"\\nUnexpected error: {e}")