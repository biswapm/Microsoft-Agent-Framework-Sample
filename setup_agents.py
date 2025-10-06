"""
Create Agent Directory Structure for DevUI Discovery
Sets up agents in the format that DevUI can automatically discover.
"""

import os
import asyncio
from dotenv import load_dotenv


def create_agent_directories():
    """Create the directory structure for DevUI agent discovery."""
    
    print("🏗️ Creating Agent Directory Structure...")
    print("=" * 45)
    
    # Create main agents directory
    agents_dir = "agents"
    if not os.path.exists(agents_dir):
        os.makedirs(agents_dir)
        print(f"✅ Created {agents_dir}/ directory")
    
    # Create Interactive Researcher Agent
    researcher_dir = os.path.join(agents_dir, "interactive_researcher")
    if not os.path.exists(researcher_dir):
        os.makedirs(researcher_dir)
        print(f"✅ Created {researcher_dir}/ directory")
    
    # Create __init__.py for interactive researcher
    researcher_init = f"""\"\"\"Interactive Researcher Agent for DevUI Discovery.\"\"\"

import os
from dotenv import load_dotenv
from agent_framework_azure_ai import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Load environment variables
load_dotenv()

# Create the Interactive Researcher agent
agent = AzureAIAgentClient(
    deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini"),
    instructions=\"\"\"
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
    \"\"\",
    credential=AzureCliCredential()
)
"""
    
    with open(os.path.join(researcher_dir, "__init__.py"), "w") as f:
        f.write(researcher_init)
    print(f"✅ Created {researcher_dir}/__init__.py")
    
    # Create LangChain Blog Agent directory
    blog_dir = os.path.join(agents_dir, "langchain_blog_agent")
    if not os.path.exists(blog_dir):
        os.makedirs(blog_dir)
        print(f"✅ Created {blog_dir}/ directory")
    
    # Create __init__.py for blog agent
    blog_init = f"""\"\"\"LangChain Blog Agent for DevUI Discovery.\"\"\"

import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

@tool
def format_blog_post(content: str, title: str = None) -> str:
    \"\"\"Format content into a well-structured blog post with proper markdown.\"\"\"
    if title:
        formatted = f"# {{title}}\\n\\n{{content}}"
    else:
        formatted = content
    
    # Add proper markdown formatting
    lines = formatted.split('\\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip() and not line.startswith('#') and not line.startswith('-') and not line.startswith('*'):
            if len(line) > 100:
                formatted_lines.append(f"{{line}}\\n")
            else:
                formatted_lines.append(line)
        else:
            formatted_lines.append(line)
    
    return '\\n'.join(formatted_lines)

@tool
def add_seo_elements(content: str, keywords: list = None) -> str:
    \"\"\"Add SEO-friendly elements to blog content.\"\"\"
    if not keywords:
        keywords = ["artificial intelligence", "technology", "innovation"]
    
    seo_content = content
    
    # Add meta description suggestion
    meta_desc = f"Learn about {{', '.join(keywords[:3])}} in this comprehensive guide."
    seo_content += f"\\n\\n<!-- Suggested Meta Description: {{meta_desc}} -->"
    
    # Add keyword suggestions
    seo_content += f"\\n\\n<!-- SEO Keywords: {{', '.join(keywords)}} -->"
    
    return seo_content

# Initialize LangChain Blog Agent
llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", \"\"\"You are an expert blog writer and content creator. 
    Transform research content into engaging, well-structured blog posts.
    Use the available tools to format content and add SEO elements.\"\"\"),
    ("human", "{{input}}"),
    ("placeholder", "{{agent_scratchpad}}")
])

tools = [format_blog_post, add_seo_elements]
agent_executor = create_openai_tools_agent(llm, tools, prompt)

# Export the agent for DevUI
agent = AgentExecutor(agent=agent_executor, tools=tools, verbose=True)
"""
    
    with open(os.path.join(blog_dir, "__init__.py"), "w") as f:
        f.write(blog_init)
    print(f"✅ Created {blog_dir}/__init__.py")
    
    print("\\n🎯 Agent directory structure created successfully!")
    print("\\nYou can now run DevUI with directory discovery:")
    print(f"   python -m agent_framework_devui {agents_dir} --port 8080")
    print("\\nOr use the main.py to load agents programmatically.")


if __name__ == "__main__":
    create_agent_directories()