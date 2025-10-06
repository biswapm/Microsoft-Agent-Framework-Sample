"""
Research to Blog Orchestrator using Sequential Workflow
Orchestrates the research agent and blog post agent to create comprehensive blog posts.
Now with LangChain Blog Agent for enhanced content creation.
"""

import asyncio
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv


class SequentialWorkflow:
    """Simple sequential workflow implementation."""
    
    def __init__(self, agents: List[Any]):
        self.agents = agents
    
    async def run(self, initial_input: str) -> List[Any]:
        """
        Run agents sequentially, passing output from one to the next.
        
        Args:
            initial_input: Initial input for the first agent
            
        Returns:
            List of results from each agent
        """
        results = []
        current_input = initial_input
        
        for i, agent in enumerate(self.agents):
            print(f"Running agent {i + 1}/{len(self.agents)}...")
            
            # Handle both async and sync agents
            if hasattr(agent, 'get_response') and asyncio.iscoroutinefunction(agent.get_response):
                # Azure AI agents use get_response method
                result = await agent.get_response(current_input)
                # Extract content from ChatResponse if needed
                if hasattr(result, 'content'):
                    result = result.content
                elif hasattr(result, 'text'):
                    result = result.text
                elif not isinstance(result, str):
                    result = str(result)
            elif hasattr(agent, 'run') and asyncio.iscoroutinefunction(agent.run):
                result = await agent.run(current_input)
                # Extract content from BlogResult if this is the blog agent
                if hasattr(result, 'text'):
                    result = result.text
                elif hasattr(result, 'content'):
                    result = result.content
                elif not isinstance(result, str):
                    result = str(result)
            elif hasattr(agent, 'sync_run'):
                result = agent.sync_run(current_input)
                # Extract content from BlogResult if this is the blog agent
                if hasattr(result, 'text'):
                    result = result.text
                elif hasattr(result, 'content'):
                    result = result.content
                elif not isinstance(result, str):
                    result = str(result)
            elif hasattr(agent, 'run'):
                result = agent.run(current_input)
                # Extract content from BlogResult if this is the blog agent
                if hasattr(result, 'text'):
                    result = result.text
                elif hasattr(result, 'content'):
                    result = result.content
                elif not isinstance(result, str):
                    result = str(result)
            else:
                # Fallback for agents without standard run method
                result = await agent(current_input)
            
            results.append(result)
            
            # For the blog agent, modify the input to include research context
            if i == 0 and len(self.agents) > 1:  # Research to Blog workflow
                # Extract content from result (handle both string and object types)
                research_content = result
                if hasattr(result, 'text'):
                    research_content = result.text
                elif hasattr(result, 'content'):
                    research_content = result.content
                elif not isinstance(result, str):
                    research_content = str(result)
                
                current_input = f"""
                Transform the following research content into an engaging blog post:
                
                Research Content:
                {research_content}
                
                Requirements:
                - Create a compelling headline and introduction
                - Use clear section headers and structure
                - Include practical examples and applications
                - Make complex concepts accessible
                - Ensure proper markdown formatting
                - Conclude with key takeaways and next steps
                
                Create a complete, publication-ready blog post.
                """
        
        return results


class ResearchToBlogOrchestrator:
    """Orchestrates research and blog post generation using Agent Framework workflows."""
    
    def __init__(self):
        self.research_agent = None
        self.blog_agent = None
    
    async def initialize(self):
        """Initialize both agents with proper configuration."""
        load_dotenv()
        
        try:
            from agent_framework.azure import AzureAIAgentClient
            from azure.identity.aio import AzureCliCredential as AsyncAzureCliCredential
        except ImportError as e:
            print(f"Import error: {e}")
            print("Please install the required packages: pip install agent-framework azure-identity")
            return
        
        print("Initializing Research Agent...")
        
        # Get required environment variables
        project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        model_deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        
        if not project_endpoint or not model_deployment:
            raise ValueError(
                "Missing required environment variables. "
                "Please set AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME"
            )
        
        # Initialize Research Agent (Azure AI Foundry) with correct pattern
        credential = AsyncAzureCliCredential()
        self.research_agent = AzureAIAgentClient(
            async_credential=credential,
            deployment_name=model_deployment,
            instructions="""
            You are a thorough research assistant. Your role is to:
            1. Research the given topic comprehensively
            2. Gather factual information from reliable sources  
            3. Identify key concepts, trends, and insights
            4. Organize findings in a clear, structured format
            5. Provide citations and references where possible
            6. Highlight practical applications and real-world examples
            
            Present your research in a well-organized format that can be used
            to create educational content.
            """
        )
        
        print("Initializing LangChain Blog Post Agent...")
        
        # Initialize LangChain Blog Agent
        try:
            from src.langchain_blog_agent import LangChainBlogAgent
            self.blog_agent = LangChainBlogAgent()
            self.blog_agent.initialize()
        except ImportError as e:
            print(f"LangChain import error: {e}")
            print("Falling back to Azure AI Agent for blog writing...")
            # Fallback to Azure AI Agent if LangChain is not available
            self.blog_agent = AzureAIAgentClient(
                async_credential=credential,
                deployment_name=model_deployment,
                instructions="""
                You are an expert blog writer and content creator. Your role is to:
                1. Transform research content into engaging blog posts
                2. Create compelling headlines and introductions
                3. Structure content with clear sections and headings
                4. Use conversational yet professional tone
                5. Include practical examples and actionable insights
                6. Format content with proper markdown
                7. Ensure content is accessible to target audience
                8. Add relevant calls-to-action and conclusions
                
                Create publication-ready blog posts that are both informative and engaging.
                """
            )
        
        print("Research Agent and LangChain Blog Agent initialized successfully!")
    
    async def create_blog_from_topic(self, topic: str) -> Dict[str, Any]:
        """
        Use Sequential Workflow to create a blog post from a research topic.
        
        Args:
            topic: Research topic to investigate and write about
            
        Returns:
            Dictionary containing research results and final blog post
        """
        if not self.research_agent or not self.blog_agent:
            await self.initialize()
        
        print(f"\n Starting sequential workflow for topic: '{topic}'")
        
        # Create sequential workflow
        workflow = SequentialWorkflow([self.research_agent, self.blog_agent])
        
        # Run the workflow
        results = await workflow.run(topic)
        
        # Extract results with proper handling for both string and object responses
        research_result = results[0] if len(results) > 0 else None
        blog_result = results[1] if len(results) > 1 else None
        
        # Helper function to extract content from various result types
        def extract_content(result):
            if result is None:
                return "No content generated"
            elif isinstance(result, str):
                return result
            elif hasattr(result, 'text'):
                return result.text
            elif hasattr(result, 'content'):
                return result.content
            else:
                return str(result)
        
        # Helper function to extract metadata
        def extract_metadata(result):
            if result is None or isinstance(result, str):
                return {}
            else:
                return getattr(result, 'metadata', {})
        
        workflow_results = {
            "topic": topic,
            "research": {
                "content": extract_content(research_result),
                "metadata": extract_metadata(research_result)
            },
            "blog_post": {
                "content": extract_content(blog_result),
                "metadata": extract_metadata(blog_result)
            },
            "workflow_status": "completed"
        }
        
        print("\n Sequential workflow completed successfully!")
        return workflow_results
    
    async def cleanup(self):
        """Clean up resources."""
        if self.research_agent:
            try:
                await self.research_agent.close()
            except:
                pass
        if self.blog_agent:
            try:
                await self.blog_agent.close()
            except:
                pass


async def demo_orchestration():
    """Demonstrate the research-to-blog orchestration."""
    
    print("Research to Blog Orchestration Demo")
    print("=" * 50)
    
    orchestrator = ResearchToBlogOrchestrator()
    
    try:
        # Demo topic
        topic = "Edge Computing in IoT Applications"
        
        print(f"\nDemo: {topic}")
        print("-" * 40)
        
        result = await orchestrator.create_blog_from_topic(topic)
        
        print(f"\nTopic: {result['topic']}")
        print(f"\nResearch Content Preview:")
        research_preview = result['research']['content'][:500] + "..." if len(result['research']['content']) > 500 else result['research']['content']
        print(research_preview)
        
        print(f"\nGenerated Blog Post:")
        print(result['blog_post']['content'])
        
        print("\n" + "="*50)
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await orchestrator.cleanup()


async def interactive_blog_creation():
    """Interactive blog creation session."""
    
    print("Interactive Research-to-Blog Creation")
    print("=" * 50)
    print("Enter a topic and I'll research it and create a blog post for you.")
    
    orchestrator = ResearchToBlogOrchestrator()
    
    try:
        while True:
            topic = input("\nEnter a topic (or 'quit' to exit): ").strip()
            
            if topic.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the Research-to-Blog Orchestrator!")
                break
            
            if not topic:
                print("Please enter a valid topic.")
                continue
            
            try:
                result = await orchestrator.create_blog_from_topic(topic)
                
                print(f"\n📝 Blog Post Created for: {result['topic']}")
                print("=" * 60)
                print(result['blog_post']['content'])
                print("=" * 60)
                
            except Exception as e:
                print(f"Error creating blog post: {e}")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await orchestrator.cleanup()


if __name__ == "__main__":
    print("Research to Blog Orchestrator - Agent Framework")
    print("=" * 55)
    print("Choose an option:")
    print("1. Run demo")
    print("2. Interactive blog creation")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\nStarting demo...")
        asyncio.run(demo_orchestration())
    elif choice == "2":
        print("\nStarting interactive mode...")
        asyncio.run(interactive_blog_creation())
    elif choice == "3":
        print("\nGoodbye!")
    else:
        print("\nInvalid choice. Starting demo...")
        asyncio.run(demo_orchestration())