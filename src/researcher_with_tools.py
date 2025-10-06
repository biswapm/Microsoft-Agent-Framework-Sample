"""
Research Agent with Custom Tools using Azure AI Foundry Agent
Demonstrates how to extend the research agent with custom function tools.
"""

import asyncio
import os
import json
from typing import Annotated, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field


# Custom research tools
def search_academic_papers(
    topic: Annotated[str, Field(description="The research topic or keywords to search for academic papers.")],
    max_results: Annotated[int, Field(description="Maximum number of papers to return (1-10).")] = 5
) -> str:
    """
    Search for academic papers related to a given topic.
    Note: This is a simulation of academic paper search functionality.
    """
    # Simulate academic paper search results
    papers = [
        {
            "title": f"Advanced Research in {topic}: A Comprehensive Analysis",
            "authors": "Smith, J., Johnson, A., Williams, B.",
            "journal": "Journal of Advanced Research",
            "year": 2024,
            "abstract": f"This paper presents a comprehensive analysis of {topic}, examining current methodologies and future directions in the field."
        },
        {
            "title": f"Machine Learning Applications in {topic}",
            "authors": "Chen, L., Rodriguez, M., Kim, S.",
            "journal": "AI Research Quarterly",
            "year": 2023,
            "abstract": f"We explore the application of machine learning techniques to {topic}, demonstrating significant improvements in accuracy and efficiency."
        },
        {
            "title": f"Emerging Trends in {topic} Research",
            "authors": "Thompson, R., Davis, K., Brown, N.",
            "journal": "Future Science Reviews",
            "year": 2024,
            "abstract": f"This review article discusses emerging trends and breakthrough discoveries in {topic} research over the past five years."
        }
    ]
    
    # Limit results based on max_results parameter
    limited_papers = papers[:min(max_results, len(papers))]
    
    result = f"Found {len(limited_papers)} academic papers related to '{topic}':\n\n"
    
    for i, paper in enumerate(limited_papers, 1):
        result += f"{i}. **{paper['title']}**\n"
        result += f"   Authors: {paper['authors']}\n"
        result += f"   Journal: {paper['journal']} ({paper['year']})\n"
        result += f"   Abstract: {paper['abstract']}\n\n"
    
    return result


def get_research_statistics(
    field: Annotated[str, Field(description="The research field or domain to get statistics for.")]
) -> str:
    """
    Get statistical information about a research field.
    Note: This simulates research statistics and metrics.
    """
    # Simulate research statistics
    stats = {
        "total_publications": 15847,
        "annual_growth_rate": "12.3%",
        "top_institutions": [
            "MIT", "Stanford University", "Carnegie Mellon University",
            "University of Cambridge", "ETH Zurich"
        ],
        "funding_amount": "$2.4 billion",
        "active_researchers": 8924,
        "emerging_subfields": [
            f"Quantum {field}",
            f"Bio-inspired {field}",
            f"Sustainable {field}"
        ]
    }
    
    result = f"Research Statistics for {field}:\n\n"
    result += f" **Key Metrics:**\n"
    result += f"- Total Publications: {stats['total_publications']:,}\n"
    result += f"- Annual Growth Rate: {stats['annual_growth_rate']}\n"
    result += f"- Total Funding: {stats['funding_amount']}\n"
    result += f"- Active Researchers: {stats['active_researchers']:,}\n\n"
    
    result += f" **Top Institutions:**\n"
    for institution in stats['top_institutions']:
        result += f"- {institution}\n"
    result += "\n"
    
    result += f" **Emerging Subfields:**\n"
    for subfield in stats['emerging_subfields']:
        result += f"- {subfield}\n"
    
    return result


def create_research_timeline(
    topic: Annotated[str, Field(description="The research topic to create a timeline for.")],
    start_year: Annotated[int, Field(description="Starting year for the timeline.")] = 2020
) -> str:
    """
    Create a research timeline showing key developments in a field.
    Note: This simulates a research timeline with key milestones.
    """
    current_year = datetime.now().year
    
    # Simulate timeline events
    timeline_events = []
    for year in range(start_year, current_year + 1):
        if year % 2 == 0:  # Add events for even years
            timeline_events.append({
                "year": year,
                "event": f"Major breakthrough in {topic} methodology",
                "description": f"Researchers developed new approaches to {topic} that improved efficiency by 25%."
            })
        else:  # Add events for odd years
            timeline_events.append({
                "year": year,
                "event": f"Industry adoption of {topic} technologies",
                "description": f"Major tech companies began implementing {topic} solutions in production systems."
            })
    
    result = f"📅 Research Timeline for {topic} ({start_year}-{current_year}):\n\n"
    
    for event in timeline_events:
        result += f"**{event['year']}** - {event['event']}\n"
        result += f"   {event['description']}\n\n"
    
    return result


async def create_researcher_with_tools():
    """
    Creates a research agent with custom function tools.
    
    Returns:
        The configured research agent with tools
    """
    load_dotenv()
    
    # Verify required environment variables
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model_deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    if not project_endpoint or not model_deployment:
        raise ValueError(
            "Missing required environment variables. "
            "Please set AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME"
        )
    
    # Create Azure credential
    credential = AzureCliCredential()
    
    # Create the research agent with custom tools
    agent_client = AzureAIAgentClient(
        project_endpoint=project_endpoint,
        model_deployment_name=model_deployment,
        async_credential=credential
    )
    
    # Enhanced research instructions with tool awareness
    research_instructions = """
    You are an advanced research assistant with access to specialized research tools.
    
    Your capabilities include:
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
    
    # Create agent with custom research tools
    return agent_client.create_agent(
        name="AdvancedResearcher",
        instructions=research_instructions,
        tools=[
            search_academic_papers,
            get_research_statistics,
            create_research_timeline
        ]
    )


async def conduct_advanced_research(query: str) -> str:
    """
    Conducts advanced research using the agent with custom tools.
    
    Args:
        query: The research question or topic
    
    Returns:
        Comprehensive research results
    """
    async with (
        AzureCliCredential() as credential,
        await create_researcher_with_tools() as agent,
    ):
        print(f"🔍 Advanced Research: {query}")
        print("🛠️  Using custom research tools...")
        print("=" * 50)
        
        result = await agent.run(query)
        return result.text


async def demo_tool_capabilities():
    """Demonstrate the capabilities of individual research tools."""
    
    print("Research Tools Demonstration")
    print("=" * 50)
    
    # Demo academic paper search
    print("\n📚 Academic Paper Search Demo:")
    print("-" * 30)
    papers = search_academic_papers("artificial intelligence", 3)
    print(papers)
    
    # Demo research statistics
    print("\n Research Statistics Demo:")
    print("-" * 30)
    stats = get_research_statistics("machine learning")
    print(stats)
    
    # Demo research timeline
    print("\n Research Timeline Demo:")
    print("-" * 30)
    timeline = create_research_timeline("deep learning", 2020)
    print(timeline)


async def main():
    """Main function to demonstrate the advanced research agent."""
    
    print("Advanced Research Agent with Custom Tools")
    print("=" * 60)
    print("1. Run advanced research queries")
    print("2. Demo individual tool capabilities")
    print("=" * 60)
    
    choice = input("Choose an option (1 or 2): ").strip()
    
    if choice == "2":
        await demo_tool_capabilities()
        return
    
    # Example research queries that will use the custom tools
    research_queries = [
        "Provide a comprehensive analysis of quantum computing research including recent papers, statistics, and timeline",
        "Research the field of computer vision: current trends, key publications, and historical development",
        "Give me an overview of natural language processing research with academic papers and field metrics"
    ]
    
    try:
        for query in research_queries:
            print(f"\nResearch Query: {query}")
            print("-" * 50)
            
            result = await conduct_advanced_research(query)
            print(result)
            print("\n" + "="*60)
            
            # Pause between queries
            await asyncio.sleep(2)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPlease ensure:")
        print("1. You've configured your .env file with valid Azure AI settings")
        print("2. You're authenticated with Azure CLI (run 'az login')")
        print("3. Your Azure AI project has the specified model deployment")


if __name__ == "__main__":
    asyncio.run(main())