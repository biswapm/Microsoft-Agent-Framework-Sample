"""
Test script for LangChain Blog Agent Integration
Tests the functionality with simple content transformation.
"""

import asyncio
import os
from dotenv import load_dotenv


def test_langchain_simple():
    """Test LangChain blog agent with a simple approach."""
    load_dotenv()
    
    try:
        from langchain_openai import AzureChatOpenAI
        from azure.identity import AzureCliCredential
        
        # Get configuration
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
        
        if not azure_endpoint:
            print("❌ AZURE_OPENAI_ENDPOINT not found in environment variables")
            return
        
        print(f"✅ Azure OpenAI Endpoint: {azure_endpoint}")
        print(f"✅ Deployment: {deployment_name}")
        
        # Create credential and get token
        credential = AzureCliCredential()
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        
        # Create LLM
        llm = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=deployment_name,
            openai_api_version="2024-02-01",
            azure_ad_token=token.token,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Test with simple content
        test_content = """
        Transform the following research into a blog post:
        
        Edge Computing Research:
        - Reduces latency by 50-80% compared to cloud processing
        - Market expected to reach $43.4 billion by 2027
        - Key benefits: real-time processing, bandwidth savings, improved privacy
        - Main challenges: security and infrastructure complexity
        - Use cases: smart cities, autonomous vehicles, industrial IoT
        
        Create an engaging blog post with proper structure and markdown formatting.
        """
        
        print("🔄 Testing LangChain Azure OpenAI connection...")
        result = llm.invoke(test_content)
        
        print("✅ LangChain test successful!")
        print("Generated Content:")
        print("=" * 50)
        print(result.content)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing LangChain: {e}")
        return False


async def test_orchestrator_with_langchain():
    """Test the orchestrator with LangChain integration."""
    
    print("Testing Research-to-Blog Orchestrator with LangChain...")
    print("=" * 60)
    
    try:
        from src.research_blog_orchestrator import ResearchToBlogOrchestrator
        
        orchestrator = ResearchToBlogOrchestrator()
        await orchestrator.initialize()
        
        # Test with a simple topic
        test_topic = "Quantum Computing Applications in Finance"
        print(f"Testing with topic: {test_topic}")
        
        result = await orchestrator.create_blog_from_topic(test_topic)
        
        print("✅ Orchestrator test completed!")
        print(f"Topic: {result['topic']}")
        print(f"Research length: {len(result['research']['content'])} characters")
        print(f"Blog post length: {len(result['blog_post']['content'])} characters")
        print(f"Blog agent type: {result['blog_post']['metadata'].get('agent_type', 'unknown')}")
        
        print("\nBlog Post Preview:")
        print("-" * 40)
        blog_content = result['blog_post']['content']
        preview = blog_content[:500] + "..." if len(blog_content) > 500 else blog_content
        print(preview)
        
        await orchestrator.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error testing orchestrator: {e}")
        return False


if __name__ == "__main__":
    print("LangChain Blog Agent Test Suite")
    print("=" * 40)
    
    # Test 1: Simple LangChain connection
    print("\n1. Testing basic LangChain Azure OpenAI connection...")
    langchain_works = test_langchain_simple()
    
    if langchain_works:
        # Test 2: Full orchestrator test
        print("\n2. Testing full orchestrator with LangChain...")
        asyncio.run(test_orchestrator_with_langchain())
    else:
        print("\n❌ Skipping orchestrator test due to LangChain connection issues")
        print("Please check your Azure OpenAI configuration and Azure CLI authentication")
    
    print("\n" + "=" * 40)
    print("Test completed!")