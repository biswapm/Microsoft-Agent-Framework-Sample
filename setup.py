"""
Setup script for the Research Agent project.
Helps users configure their environment and verify dependencies.
"""

import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_azure_cli():
    """Check if Azure CLI is installed and user is logged in."""
    try:
        # Check if az command exists
        result = subprocess.run(["az", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ Azure CLI not found")
            print("   Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
            return False
        
        print("✅ Azure CLI is installed")
        
        # Check if user is logged in
        result = subprocess.run(["az", "account", "show"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("⚠️  Not logged into Azure CLI")
            print("   Run: az login")
            return False
        
        print("✅ Logged into Azure CLI")
        return True
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Azure CLI not found or not responding")
        print("   Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
        return False


def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Dependency installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def setup_environment():
    """Set up environment configuration."""
    env_example_path = Path(".env.example")
    env_path = Path(".env")
    
    if not env_example_path.exists():
        print("❌ .env.example file not found")
        return False
    
    if env_path.exists():
        print("⚠️  .env file already exists")
        overwrite = input("   Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("   Keeping existing .env file")
            return True
    
    try:
        # Copy .env.example to .env
        with open(env_example_path, 'r') as src:
            content = src.read()
        
        with open(env_path, 'w') as dst:
            dst.write(content)
        
        print("✅ Created .env file from .env.example")
        print("   📝 Please edit .env with your Azure AI settings")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def verify_configuration():
    """Verify that configuration is complete."""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "AZURE_AI_PROJECT_ENDPOINT",
        "AZURE_AI_MODEL_DEPLOYMENT_NAME"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("<") or "your-project" in value:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Configuration incomplete:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n   Please edit your .env file with actual values")
        return False
    
    print("✅ Configuration appears complete")
    return True


def main():
    """Main setup function."""
    print("🔧 Research Agent Setup")
    print("=" * 40)
    
    success = True
    
    # Check Python version
    print("\n1. Checking Python version...")
    if not check_python_version():
        success = False
    
    # Check Azure CLI
    print("\n2. Checking Azure CLI...")
    if not check_azure_cli():
        success = False
    
    # Install dependencies
    print("\n3. Installing dependencies...")
    if not install_dependencies():
        success = False
    
    # Setup environment
    print("\n4. Setting up environment...")
    if not setup_environment():
        success = False
    
    # Verify configuration
    print("\n5. Verifying configuration...")
    config_ok = verify_configuration()
    
    # Summary
    print("\n" + "=" * 40)
    if success and config_ok:
        print("🎉 Setup completed successfully!")
        print("\n📚 Next steps:")
        print("   1. Edit .env file with your Azure AI settings")
        print("   2. Run: python main.py")
    elif success:
        print("⚠️  Setup mostly completed")
        print("\n📝 Action required:")
        print("   1. Edit .env file with your Azure AI settings")
        print("   2. Run: python main.py")
    else:
        print("❌ Setup encountered issues")
        print("\n🔧 Please resolve the issues above and run setup again")
    
    print("=" * 40)


if __name__ == "__main__":
    main()