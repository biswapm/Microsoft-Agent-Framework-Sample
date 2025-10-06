"""Research to Blog Orchestrator Workflow for DevUI."""

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
