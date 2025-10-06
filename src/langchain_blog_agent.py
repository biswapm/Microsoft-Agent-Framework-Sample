"""
LangChain Blog Agent
A blog writing agent using LangChain framework for enhanced content creation.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.tools import tool


@tool
def format_blog_post(content: str, title: str = None) -> str:
    """
    Format content into a well-structured blog post with proper markdown.
    
    Args:
        content: The main content to format
        title: Optional title for the blog post
    
    Returns:
        Formatted blog post content
    """
    lines = content.split('\n')
    formatted_lines = []
    
    # Add title if provided
    if title:
        formatted_lines.append(f"# {title}")
        formatted_lines.append("")
    
    for line in lines:
        line = line.strip()
        if line:
            # Convert simple headers
            if line.startswith('**') and line.endswith('**'):
                formatted_lines.append(f"## {line[2:-2]}")
            # Add bullet points for lists
            elif line.startswith('- '):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
            formatted_lines.append("")
    
    return '\n'.join(formatted_lines)


@tool
def add_seo_elements(content: str, keywords: list = None) -> str:
    """
    Add SEO-friendly elements to blog content.
    
    Args:
        content: The blog content
        keywords: Optional list of keywords to emphasize
    
    Returns:
        Content with SEO enhancements
    """
    if not keywords:
        keywords = []
    
    # Simple SEO enhancement - this could be more sophisticated
    lines = content.split('\n')
    enhanced_lines = []
    
    for line in lines:
        if line.strip():
            # Emphasize keywords
            for keyword in keywords:
                if keyword.lower() in line.lower() and not line.startswith('#'):
                    line = line.replace(keyword, f"**{keyword}**")
            enhanced_lines.append(line)
        else:
            enhanced_lines.append(line)
    
    return '\n'.join(enhanced_lines)


class LangChainBlogAgent:
    """A blog writing agent using LangChain framework."""
    
    def __init__(self):
        self.llm = None
        self.agent = None
        self.agent_executor = None
        
    def initialize(self):
        """Initialize the LangChain blog agent."""
        load_dotenv()
        
        # Get Azure OpenAI configuration
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        if not azure_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
        
        print(f"Initializing LangChain with endpoint: {azure_endpoint}")
        print(f"Using deployment: {deployment_name}")
        
        # Try different authentication methods
        if api_key:
            print("Using API key authentication...")
            self.llm = AzureChatOpenAI(
                azure_endpoint=azure_endpoint,
                azure_deployment=deployment_name,
                openai_api_version="2024-02-01",
                api_key=api_key,
                temperature=0.7,
                max_tokens=2000
            )
        else:
            print("No API key found. Trying Azure CLI authentication...")
            try:
                from azure.identity import AzureCliCredential
                
                # Use Azure CLI credential for authentication
                credential = AzureCliCredential()
                
                # Get access token for Azure OpenAI
                token = credential.get_token("https://cognitiveservices.azure.com/.default")
                
                self.llm = AzureChatOpenAI(
                    azure_endpoint=azure_endpoint,
                    azure_deployment=deployment_name,
                    openai_api_version="2024-02-01",
                    azure_ad_token=token.token,
                    temperature=0.7,
                    max_tokens=2000
                )
                
            except Exception as e:
                print(f"Error with Azure CLI authentication: {e}")
                raise ValueError(
                    "No valid authentication method found. Please either:\\n"
                    "1. Set AZURE_OPENAI_API_KEY environment variable, or\\n"
                    "2. Configure Azure CLI with 'az login'"
                )
        
        # Define the system prompt for blog writing
        system_prompt = """
        You are an expert blog writer and content creator specializing in technology topics.
        Your expertise includes:
        
        1. **Content Structure**: Creating compelling headlines, engaging introductions, 
           clear section headers, and strong conclusions
        2. **Writing Style**: Conversational yet professional tone that makes complex 
           concepts accessible to general audiences
        3. **Practical Value**: Including real-world examples, actionable insights, 
           and practical applications
        4. **SEO Optimization**: Using proper markdown formatting, strategic keyword 
           placement, and reader-friendly structure
        5. **Engagement**: Adding calls-to-action, key takeaways, and future outlook
        
        When transforming research content into blog posts:
        - Start with a compelling headline that captures the essence
        - Create an engaging introduction with a hook
        - Organize content with clear, descriptive subheadings
        - Use bullet points and numbered lists for key information
        - Include practical examples and real-world applications
        - End with key takeaways and next steps
        - Ensure proper markdown formatting throughout
        
        IMPORTANT: Always return the FINAL FORMATTED BLOG CONTENT as your response, 
        not tool descriptions or summaries. After using tools to format and optimize 
        the content, provide the complete, ready-to-publish blog post.
        
        Your final response should be the complete blog post that readers will see,
        formatted in markdown with proper headings, sections, and content.
        """
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Available tools for the agent
        tools = [format_blog_post, add_seo_elements]
        
        # Create the agent
        self.agent = create_openai_tools_agent(self.llm, tools, prompt)
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            verbose=False,  # Disable verbose to avoid tool descriptions in output
            max_iterations=3,
            return_intermediate_steps=True
        )
        
        print("✅ LangChain Blog Agent initialized successfully!")
    
    async def run(self, input_text: str) -> Any:
        """
        Run the blog agent to create content.
        
        Args:
            input_text: The input content to transform into a blog post
            
        Returns:
            Blog agent result with generated content
        """
        if not self.agent_executor:
            self.initialize()
        
        try:
            # Run the agent
            result = await self.agent_executor.ainvoke({
                "input": input_text
            })
            
            # Extract the actual blog content, filtering out tool descriptions
            output = result["output"]
            
            # If the output contains tool descriptions or SEO summaries, try to extract actual content
            if "The blog has been formatted" in output or "optimized for SEO" in output:
                # Look for the actual formatted content in intermediate steps
                intermediate_steps = result.get("intermediate_steps", [])
                for step in intermediate_steps:
                    if len(step) >= 2:
                        tool_input = step[0]
                        tool_output = step[1]
                        
                        # If this is a formatting tool with substantial content, use it
                        if hasattr(tool_input, 'tool') and tool_input.tool in ['format_blog_post', 'add_seo_elements']:
                            if len(str(tool_output)) > 500:  # Substantial content
                                output = str(tool_output)
                                break
            
            # Create a result object that mimics the Azure AI Agent response
            class BlogResult:
                def __init__(self, content: str, metadata: dict = None):
                    self.text = content
                    self.metadata = metadata or {}
            
            return BlogResult(
                output,  # Pass processed content as positional argument
                {
                    "agent_type": "langchain",
                    "intermediate_steps": result.get("intermediate_steps", []),
                    "tool_calls": len(result.get("intermediate_steps", []))
                }
            )
            
        except Exception as e:
            print(f"Error in LangChain blog agent: {e}")
            # Return a basic result with error info
            class BlogResult:
                def __init__(self, content: str, metadata: dict = None):
                    self.text = content
                    self.metadata = metadata or {}
            
            return BlogResult(
                f"Error generating blog post: {str(e)}",  # Pass content as positional argument
                {"error": str(e), "agent_type": "langchain"}
            )
    
    def sync_run(self, input_text: str) -> Any:
        """
        Synchronous version of run method.
        
        Args:
            input_text: The input content to transform into a blog post
            
        Returns:
            Blog agent result with generated content
        """
        if not self.agent_executor:
            self.initialize()
        
        try:
            # Run the agent synchronously
            result = self.agent_executor.invoke({
                "input": input_text
            })
            
            # Create a result object that mimics the Azure AI Agent response
            class BlogResult:
                def __init__(self, content: str, metadata: dict = None):
                    self.text = content
                    self.metadata = metadata or {}
            
            return BlogResult(
                content=result["output"],
                metadata={
                    "agent_type": "langchain",
                    "intermediate_steps": result.get("intermediate_steps", []),
                    "tool_calls": len(result.get("intermediate_steps", []))
                }
            )
            
        except Exception as e:
            print(f"Error in LangChain blog agent: {e}")
            # Return a basic result with error info
            class BlogResult:
                def __init__(self, content: str, metadata: dict = None):
                    self.text = content
                    self.metadata = metadata or {}
            
            return BlogResult(
                content=f"Error generating blog post: {str(e)}",
                metadata={"error": str(e), "agent_type": "langchain"}
            )


# Example usage and testing
async def test_langchain_blog_agent():
    """Test the LangChain blog agent."""
    
    agent = LangChainBlogAgent()
    agent.initialize()
    
    test_research = """
    Edge Computing in IoT Applications
    
    Key findings from research:
    - Edge computing reduces latency by processing data closer to IoT devices
    - Market size expected to reach $43.4 billion by 2027
    - Main benefits include real-time processing, reduced bandwidth usage, and improved privacy
    - Key challenges include security concerns and infrastructure complexity
    - Popular use cases: smart cities, autonomous vehicles, industrial IoT
    """
    
    print("Testing LangChain Blog Agent...")
    result = await agent.run(f"Transform this research into an engaging blog post: {test_research}")
    
    print("Generated Blog Post:")
    print("=" * 50)
    print(result.text)
    print("=" * 50)
    print(f"Metadata: {result.metadata}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_langchain_blog_agent())