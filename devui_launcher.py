"""
Simple DevUI Launcher
Directly starts the Agent Framework DevUI without menus.
"""

import asyncio
import os
from dotenv import load_dotenv


async def main():
    """Launch DevUI directly with sample gallery."""
    
    load_dotenv()
    
    print(" Starting Agent Framework DevUI...")
    print("=" * 40)
    
    # Check if DevUI is available
    try:
        from agent_framework_devui import serve
        print(" Agent Framework DevUI is available")
    except ImportError:
        print("Agent Framework DevUI not found")
        print("Please install: pip install agent-framework-devui")
        return
    
    print("Starting DevUI with sample gallery...")
    print("This will show curated examples from the Agent Framework repository")
    print("Access URL: http://localhost:8080")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        # Start DevUI with empty entities (shows sample gallery) - no Azure credentials needed
        serve(entities=[], auto_open=True, port=8080)
        
    except Exception as e:
        print(f" DevUI failed to start: {e}")
        print("\\nTroubleshooting:")
        print("1. Check if port 8080 is available")
        print("2. Verify agent-framework-devui is installed")
        print("3. Try a different port")


if __name__ == "__main__":
    asyncio.run(main())