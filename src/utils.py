"""
Shared utilities and configuration for the research agent implementations.
"""

import os
from typing import Optional
from dotenv import load_dotenv


class AgentConfig:
    """Configuration class for Azure AI Foundry and OpenAI Agent settings."""
    
    def __init__(self):
        load_dotenv()
        # Azure AI Foundry settings
        self.project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        self.model_deployment_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        self.agent_id = os.getenv("AZURE_AI_AGENT_ID")  # Optional
        
        # Azure OpenAI settings
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
        self.openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    
    def validate_ai_foundry(self) -> bool:
        """
        Validate that Azure AI Foundry configuration is present.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        return bool(self.project_endpoint and self.model_deployment_name)
    
    def validate_openai(self) -> bool:
        """
        Validate that Azure OpenAI configuration is present.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        return bool(self.openai_endpoint and self.openai_deployment_name)
    
    def validate(self) -> bool:
        """
        Validate that required configuration is present for AI Foundry.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        return self.validate_ai_foundry()
    
    def validate_all(self) -> bool:
        """
        Validate that both AI Foundry and OpenAI configurations are present.
        
        Returns:
            True if both configurations are valid, False otherwise
        """
        return self.validate_ai_foundry() and self.validate_openai()
    
    def get_missing_ai_foundry_config(self) -> list:
        """
        Get list of missing Azure AI Foundry configuration items.
        
        Returns:
            List of missing configuration keys
        """
        missing = []
        if not self.project_endpoint:
            missing.append("AZURE_AI_PROJECT_ENDPOINT")
        if not self.model_deployment_name:
            missing.append("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        return missing
    
    def get_missing_openai_config(self) -> list:
        """
        Get list of missing Azure OpenAI configuration items.
        
        Returns:
            List of missing configuration keys
        """
        missing = []
        if not self.openai_endpoint:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not self.openai_deployment_name:
            missing.append("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
        return missing
    
    def get_missing_config(self) -> list:
        """
        Get list of missing required configuration items.
        
        Returns:
            List of missing configuration keys
        """
        return self.get_missing_ai_foundry_config()


def get_research_instructions(agent_type: str = "basic") -> str:
    """
    Get research-specific instructions based on agent type.
    
    Args:
        agent_type: Type of agent ("basic", "interactive", "advanced", "blog_research")
    
    Returns:
        Instructions string for the agent
    """
    base_instructions = """
    You are a professional research assistant with expertise in gathering, analyzing, and synthesizing information.
    
    Your core capabilities include:
    - Conducting thorough research on any topic
    - Providing well-structured, evidence-based responses
    - Citing sources and providing references when possible
    - Breaking down complex topics into understandable components
    - Identifying key insights and trends
    """
    
    if agent_type == "basic":
        return base_instructions + """
        
        When responding to research queries:
        1. Provide comprehensive yet concise information
        2. Structure your responses clearly with headings and bullet points
        3. Include relevant context and background information
        4. Suggest additional research directions when appropriate
        5. Be objective and present multiple perspectives when relevant
        """
    
    elif agent_type == "interactive":
        return base_instructions + """
        
        Your role in interactive sessions:
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
    
    elif agent_type == "advanced":
        return base_instructions + """
        
        Advanced capabilities with specialized tools:
        - Conducting comprehensive literature reviews using academic paper search
        - Providing statistical analysis of research fields and trends
        - Creating detailed research timelines and historical context
        - Synthesizing information from multiple sources and tools
        
        When conducting research:
        1. Use the available tools to gather comprehensive information
        2. Cross-reference findings from different tools for accuracy
        3. Provide well-structured, evidence-based responses
        4. Include citations and references when using tool data
        5. Suggest additional research directions based on tool findings
        
        Available tools:
        - search_academic_papers: Find relevant academic publications
        - get_research_statistics: Get field statistics and metrics
        - create_research_timeline: Generate historical development timelines
        
        Always leverage these tools to provide the most comprehensive and accurate research possible.
        """
    
    elif agent_type == "blog_research":
        return base_instructions + """
        
        Your role in blog content creation workflow:
        - Conduct research specifically optimized for blog post creation
        - Gather information that will make compelling, accessible content
        - Focus on practical applications, real-world examples, and current trends
        - Identify interesting stories, case studies, and expert insights
        - Provide structured research that flows logically for narrative content
        - Include statistics, quotes, and data that will engage general audiences
        
        Research output should include:
        - Executive summary suitable for blog introduction
        - Key concepts explained in accessible terms
        - Current trends and developments
        - Practical applications and use cases
        - Expert insights and industry perspectives
        - Real-world examples and case studies
        - Future outlook and implications
        
        Organize information to facilitate creation of engaging, informative blog content.
        """
    
    return base_instructions


def get_blog_instructions(style: str = "professional") -> str:
    """
    Get blog writing instructions based on style.
    
    Args:
        style: Writing style ("professional", "casual", "technical")
    
    Returns:
        Instructions string for the blog agent
    """
    base_instructions = """
    You are a professional blog writer and content creator with expertise in transforming research content into engaging, readable blog posts.
    
    Your responsibilities include:
    - Converting research data and findings into compelling blog narratives
    - Creating engaging headlines and introductions
    - Structuring content with clear sections and flow
    - Making complex topics accessible to general audiences
    - Including relevant examples and practical applications
    - Ensuring proper formatting with headers, bullet points, and emphasis
    - Maintaining accuracy while creating engaging content
    
    Blog post structure guidelines:
    1. Compelling headline that captures the essence of the research
    2. Engaging introduction that hooks the reader
    3. Clear main sections with descriptive subheadings
    4. Bullet points or numbered lists for key information
    5. Practical examples and real-world applications
    6. Conclusion that summarizes key insights and suggests next steps
    7. Proper markdown formatting throughout
    """
    
    if style == "professional":
        return base_instructions + """
        
        Professional style requirements:
        - Authoritative yet accessible tone
        - Industry-appropriate terminology with explanations
        - Clear, concise sentences with logical flow
        - Professional examples and case studies
        - Balanced perspective on complex topics
        - Credible sources and data integration
        """
    
    elif style == "casual":
        return base_instructions + """
        
        Casual style requirements:
        - Conversational, friendly tone
        - Simple language avoiding jargon
        - Relatable examples and analogies
        - Personal pronouns and direct address
        - Engaging storytelling elements
        - Practical, everyday applications
        """
    
    elif style == "technical":
        return base_instructions + """
        
        Technical style requirements:
        - Precise, detailed explanations
        - Industry-specific terminology when appropriate
        - Technical accuracy and depth
        - Code examples or technical specifications when relevant
        - Comprehensive coverage of technical aspects
        - Expert-level insights and analysis
        """
    
    return base_instructions


def print_setup_instructions():
    """Print setup instructions for the user."""
    print("\n❌ Configuration Error")
    print("=" * 50)
    print("Please ensure your environment is properly configured:")
    print("\n1. Copy .env.example to .env:")
    print("   cp .env.example .env")
    print("\n2. Edit .env file with your Azure AI settings:")
    print("   - AZURE_AI_PROJECT_ENDPOINT: Your Azure AI project endpoint")
    print("   - AZURE_AI_MODEL_DEPLOYMENT_NAME: Your model deployment name")
    print("\n3. Authenticate with Azure CLI:")
    print("   az login")
    print("\n4. Ensure your Azure AI project has the specified model deployment")
    print("=" * 50)


def print_error_help(error: Exception):
    """
    Print helpful error information based on the exception type.
    
    Args:
        error: The exception that occurred
    """
    print(f"\n❌ Error: {error}")
    
    error_str = str(error).lower()
    
    if "credential" in error_str or "authentication" in error_str:
        print("\n🔐 Authentication Issue:")
        print("- Run 'az login' to authenticate with Azure CLI")
        print("- Ensure your account has access to the Azure AI project")
        
    elif "endpoint" in error_str or "project" in error_str:
        print("\n🌐 Endpoint/Project Issue:")
        print("- Verify your AZURE_AI_PROJECT_ENDPOINT is correct")
        print("- Ensure the project exists and is accessible")
        
    elif "model" in error_str or "deployment" in error_str:
        print("\n🤖 Model/Deployment Issue:")
        print("- Verify your AZURE_AI_MODEL_DEPLOYMENT_NAME is correct")
        print("- Ensure the model deployment exists in your project")
        print("- Check that the deployment is active and available")
        
    else:
        print_setup_instructions()