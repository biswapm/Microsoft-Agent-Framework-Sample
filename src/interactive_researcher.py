"""
Interactive Research Agent using Azure AI Foundry Agent
Provides a conversational interface for conducting research with follow-up questions.
"""

import asyncio
import os
from dotenv import load_dotenv
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential


class InteractiveResearcher:
    """Interactive research agent that maintains conversation context."""
    
    def __init__(self):
        self.agent = None
        self.credential = None
        
    async def initialize(self):
        """Initialize the research agent with Azure AI Foundry."""
        load_dotenv()
        
        # Enhanced research instructions for interactive sessions
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
        
        # Verify required environment variables
        project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        model_deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        
        if not project_endpoint or not model_deployment:
            raise ValueError(
                "Missing required environment variables. "
                "Please set AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME"
            )
        
        # Create Azure credential
        self.credential = AzureCliCredential()
        
        # Create the research agent using the correct pattern from GitHub example
        agent_client = AzureAIAgentClient(
            async_credential=self.credential,
            deployment_name=model_deployment,
            instructions=research_instructions
        )
        
        self.agent = agent_client
    
    async def research(self, query: str) -> str:
        """
        Conduct research with the given query.
        
        Args:
            query: The research question or topic
            
        Returns:
            Research response as text
        """
        if not self.agent:
            await self.initialize()
            
        response = await self.agent.get_response(query)
        # Extract text content from ChatResponse object
        if hasattr(response, 'content'):
            return response.content
        elif hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'message'):
            return response.message
        else:
            return str(response)
    
    async def research_stream(self, query: str):
        """
        Conduct research with streaming response.
        
        Args:
            query: The research question or topic
        """
        if not self.agent:
            await self.initialize()
            
        print(" Researching: ", end="", flush=True)
        
        # Use streaming response from GitHub example pattern
        async for chunk in self.agent.get_streaming_response(query):
            if str(chunk):
                print(str(chunk), end="", flush=True)
        print()  # New line after streaming
    
    async def cleanup(self):
        """Clean up resources."""
        if self.agent:
            try:
                await self.agent.close()
            except:
                pass
        if self.credential:
            try:
                await self.credential.close()
            except:
                pass


async def interactive_session():
    """Run an interactive research session."""
    
    researcher = InteractiveResearcher()
    
    print(" Interactive Research Agent - Azure AI Foundry")
    print("=" * 60)
    print("Welcome to your interactive research session!")
    print("Ask me anything, and I'll help you research it thoroughly.")
    print("Type 'exit', 'quit', or 'bye' to end the session.")
    print("Type 'stream' before your question for real-time responses.")
    print("=" * 60)
    
    try:
        await researcher.initialize()
        
        while True:
            print("\n What would you like to research?")
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', '']:
                print("\n Thank you for using the Interactive Research Agent!")
                break
            
            # Check for streaming mode
            if user_input.lower().startswith('stream '):
                query = user_input[7:]  # Remove 'stream ' prefix
                print(f"\n Streaming research for: {query}")
                print("-" * 50)
                await researcher.research_stream(query)
            else:
                print(f"\n🔍 Researching: {user_input}")
                print("-" * 50)
                
                response = await researcher.research(user_input)
                print(f"Research Agent: {response}")
            
            print("\n" + "="*60)
            
    except KeyboardInterrupt:
        print("\n\n Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nPlease ensure:")
        print("1. You've configured your .env file with valid Azure AI settings")
        print("2. You're authenticated with Azure CLI (run 'az login')")
        print("3. Your Azure AI project has the specified model deployment")
    finally:
        await researcher.cleanup()


async def main():
    """Main function to start the interactive research session."""
    await interactive_session()


if __name__ == "__main__":
    asyncio.run(main())