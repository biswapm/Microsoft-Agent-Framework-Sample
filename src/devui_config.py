"""
DevUI Configuration for Research to Blog Orchestrator
Sets up the Agent Framework         # Start DevUI using the serve function (this will block and auto-open browser)
        serve(entities=entities, auto_open=True, port=8080)
        
    except Exception as e:
        print(f"⚠️ Error starting DevUI with agents: {e}")
        print("\\nStarting DevUI with sample gallery instead...")
        print("💡 This will show curated examples from the Agent Framework repository")
        print("\\n🌐 Access URL: http://localhost:8080")
        print("🛑 Press Ctrl+C to stop")
        
        # Fallback: Start DevUI with empty entities (shows sample gallery)
        try:
            serve(entities=[], auto_open=True, port=8080)
        except Exception as e2:
            print(f"❌ DevUI completely failed: {e2}")
            print("\\nTroubleshooting:")
            print("1. Ensure Azure CLI is installed and logged in (az login)")
            print("2. Check your .env file configuration")  
            print("3. Verify agent-framework-devui is installed: pip install agent-framework-devui")for testing and monitoring.
"""

import asyncio
import os
from dotenv import load_dotenv


async def setup_devui():
    """Setup and start the Agent Framework DevUI for the orchestrator."""
    
    load_dotenv()
    
    print("Agent Framework DevUI Setup")
    print("=" * 40)
    print("This will start a web interface for testing the Research-to-Blog Orchestrator.")
    print("You can interact with agents, monitor workflows, and test functionality.")
    print()
    
    # Check if DevUI is available
    try:
        from agent_framework_devui import serve
        print("✅ Agent Framework DevUI is available")
    except ImportError:
        print("❌ Agent Framework DevUI not found")
        print("Please install: pip install agent-framework-devui")
        return
    
    # Check configuration
    missing_config = []
    required_env_vars = [
        "AZURE_AI_PROJECT_ENDPOINT",
        "AZURE_AI_MODEL_DEPLOYMENT_NAME"
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_config.append(var)
    
    if missing_config:
        print("Missing required environment variables:")
        for var in missing_config:
            print(f"   - {var}")
        print()
        print("Please check your .env file and ensure all required variables are set.")
        return
    
    print("Configuration looks good!")
    print()
    
    try:
        # Initialize the orchestrator and get agents
        from src.research_blog_orchestrator import ResearchToBlogOrchestrator
        from src.interactive_researcher import InteractiveResearcher
        
        print("Initializing agents...")
        
        # Create interactive researcher
        researcher = InteractiveResearcher()
        await researcher.initialize()
        
        # Create orchestrator
        orchestrator = ResearchToBlogOrchestrator()
        await orchestrator.initialize()
        
        # Collect entities for DevUI
        entities = []
        if researcher.agent:
            entities.append(researcher.agent)
        if orchestrator.research_agent:
            entities.append(orchestrator.research_agent)
        if orchestrator.blog_agent:
            entities.append(orchestrator.blog_agent)
        
        if not entities:
            print("Warning: No entities available for DevUI")
            print("You may need to configure Azure credentials first")
            return
        
        print(f"Found {len(entities)} entities for DevUI")
        print("Starting DevUI server...")
        print("\n Access URL: http://localhost:8080")
        print("The browser should open automatically.")
        print("Press Ctrl+C to stop the server")
        print()
        
        # Start DevUI using the serve function (this will block and auto-open browser)
        serve(entities=entities, auto_open=True, port=8080)
        
    except Exception as e:
        print(f" Error starting DevUI: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Azure CLI is installed and logged in (az login)")
        print("2. Check your .env file configuration")
        print("3. Verify agent-framework-devui is installed: pip install agent-framework-devui --pre")


async def setup_agent_directory():
    """Create proper directory structure for DevUI CLI discovery."""
    
    import os
    
    print("Setting up DevUI Agent Directory Structure")
    print("=" * 45)
    
    # Create agents directory
    agents_dir = "agents"
    if not os.path.exists(agents_dir):
        os.makedirs(agents_dir)
        print(f"Created {agents_dir}/ directory")
    
    # Create interactive_researcher directory
    researcher_dir = os.path.join(agents_dir, "interactive_researcher")
    if not os.path.exists(researcher_dir):
        os.makedirs(researcher_dir)
        print(f"Created {researcher_dir}/ directory")
    
    # Create __init__.py for interactive researcher
    init_content = '''"""Interactive Researcher Agent for DevUI."""

import asyncio
import os
from dotenv import load_dotenv
from agent_framework_azure_ai import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Load environment variables
load_dotenv()

# Research instructions
research_instructions = """
You are an expert research assistant specialized in interactive research sessions.

Your role is to:
- Engage in natural, flowing conversations about research topics
- Build upon previous questions and maintain context throughout the session
- Ask clarifying questions when the research scope needs refinement
- Provide progressively deeper insights as the conversation develops
- Suggest related research areas and follow-up questions
- Adapt your research depth based on the user's expertise level

Communication style:
- Be conversational yet professional
- Use clear, structured responses with headings and bullet points
- Acknowledge previous parts of the conversation when relevant
- Offer multiple perspectives on complex topics
- Provide actionable insights and recommendations

Remember: This is an ongoing research conversation, so build on what we've already discussed.
"""

# Create the agent
agent = AzureAIAgentClient(
    deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini"),
    instructions=research_instructions,
    credential=AzureCliCredential()
)
'''
    
    init_file = os.path.join(researcher_dir, "__init__.py")
    with open(init_file, "w") as f:
        f.write(init_content)
    print(f"Created {init_file}")
    
    # Create orchestrator directory
    orchestrator_dir = os.path.join(agents_dir, "research_blog_orchestrator")
    if not os.path.exists(orchestrator_dir):
        os.makedirs(orchestrator_dir)
        print(f"Created {orchestrator_dir}/ directory")
    
    # Create __init__.py for orchestrator (workflow)
    workflow_content = '''"""Research to Blog Orchestrator Workflow for DevUI."""

import os
from dotenv import load_dotenv
from agent_framework import WorkflowBuilder
from agent_framework_azure_ai import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Load environment variables
load_dotenv()

# Create research agent
research_agent = AzureAIAgentClient(
    deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini"),
    instructions="""You are a thorough research assistant. Research topics comprehensively, 
    gather factual information, identify key concepts and trends, and organize findings clearly.""",
    credential=AzureCliCredential()
)

# Create blog agent
blog_agent = AzureAIAgentClient(
    deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini"),
    instructions="""You are an expert blog writer. Transform research content into engaging blog posts 
    with compelling headlines, clear structure, and practical examples.""",
    credential=AzureCliCredential()
)

# Create workflow
workflow = WorkflowBuilder().add_agent(research_agent).add_agent(blog_agent).build()
'''
    
    workflow_file = os.path.join(orchestrator_dir, "__init__.py")
    with open(workflow_file, "w") as f:
        f.write(workflow_content)
    print(f"Created {workflow_file}")
    
async def test_orchestrator_with_devui():
    """Test the orchestrator functionality with DevUI monitoring."""
    
    try:
        from src.research_blog_orchestrator import ResearchToBlogOrchestrator
        
        print("Testing Research-to-Blog Orchestrator...")
        print("=" * 45)
        
        orchestrator = ResearchToBlogOrchestrator()
        await orchestrator.initialize()
        
        # Test with a simple topic
        test_topic = "Artificial Intelligence in Healthcare"
        print(f"Testing with topic: {test_topic}")
        
        result = await orchestrator.create_blog_from_topic(test_topic)
        
        print(f" Orchestrator test completed!")
        print(f"Generated blog post length: {len(result['blog_post']['content'])} characters")
        
        await orchestrator.cleanup()
        
    except Exception as e:
        print(f" Error testing orchestrator: {e}")


async def start_devui_cli():
    """Start DevUI using CLI method for directory discovery."""
    
    print("Starting DevUI CLI Method")
    print("=" * 30)
    
    # First create the agent directory structure
    await setup_agent_directory()
    
    print("\nStarting DevUI server...")
    try:
        import subprocess
        import sys
        
        # Use subprocess to run devui CLI
        result = subprocess.run([
            sys.executable, "-m", "agent_framework_devui", 
            "agents", "--port", "8080", "--auto-open"
        ], check=False)
        
        if result.returncode != 0:
            print("DevUI CLI failed, trying programmatic method...")
            await setup_devui()
            
    except Exception as e:
        print(f"Error with CLI method: {e}")
        print("Falling back to programmatic method...")
        await setup_devui()
    """Test the orchestrator functionality with DevUI monitoring."""
    
    try:
        from src.research_blog_orchestrator import ResearchToBlogOrchestrator
        
        print("Testing Research-to-Blog Orchestrator...")
        print("=" * 45)
        
        orchestrator = ResearchToBlogOrchestrator()
        await orchestrator.initialize()
        
        # Test with a simple topic
        test_topic = "Artificial Intelligence in Healthcare"
        print(f"Testing with topic: {test_topic}")
        
        result = await orchestrator.create_blog_from_topic(test_topic)
        
        print(f" Orchestrator test completed!")
        print(f"Generated blog post length: {len(result['blog_post']['content'])} characters")
        
        await orchestrator.cleanup()
        
    except Exception as e:
        print(f" Error testing orchestrator: {e}")


if __name__ == "__main__":
    print("DevUI Setup Options:")
    print("1. Start DevUI Server (Programmatic)")
    print("2. Setup Agent Directory & Start DevUI CLI")
    print("3. Test Orchestrator")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(setup_devui())
    elif choice == "2":
        asyncio.run(start_devui_cli())
    elif choice == "3":
        asyncio.run(test_orchestrator_with_devui())
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Starting DevUI server...")
        asyncio.run(setup_devui())