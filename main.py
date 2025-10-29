import os
import asyncio
from datetime import datetime, timedelta
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Import tools and prompts
from tools.general_tools import get_config_value, write_config_value
from tools.config_validator import run_validation
from prompts.agent_prompt import all_crypto_symbols


# Agent class mapping table - for dynamic import and instantiation
AGENT_REGISTRY = {
    "BaseAgent": {
        "module": "agent.base_agent.base_agent",
        "class": "BaseAgent"
    },
}


def get_agent_class(agent_type):
    """
    Dynamically import and return the corresponding class based on agent type name
    
    Args:
        agent_type: Agent type name (e.g., "BaseAgent")
        
    Returns:
        Agent class
        
    Raises:
        ValueError: If agent type is not supported
        ImportError: If unable to import agent module
    """
    if agent_type not in AGENT_REGISTRY:
        supported_types = ", ".join(AGENT_REGISTRY.keys())
        raise ValueError(
            f"❌ Unsupported agent type: {agent_type}\n"
            f"   Supported types: {supported_types}"
        )
    
    agent_info = AGENT_REGISTRY[agent_type]
    module_path = agent_info["module"]
    class_name = agent_info["class"]
    
    try:
        # Dynamic import module
        import importlib
        module = importlib.import_module(module_path)
        agent_class = getattr(module, class_name)
        print(f"✅ Successfully loaded Agent class: {agent_type} (from {module_path})")
        return agent_class
    except ImportError as e:
        raise ImportError(f"❌ Unable to import agent module {module_path}: {e}")
    except AttributeError as e:
        raise AttributeError(f"❌ Class {class_name} not found in module {module_path}: {e}")


def load_config(config_path=None):
    """
    Load configuration file from configs directory
    
    Args:
        config_path: Configuration file path, if None use default config
        
    Returns:
        dict: Configuration dictionary
    """
    if config_path is None:
        # Default configuration file path - use OKX config as default
        config_path = Path(__file__).parent / "configs" / "okx_crypto_config.json"
    else:
        config_path = Path(config_path)
    
    if not config_path.exists():
        print(f"❌ Configuration file does not exist: {config_path}")
        exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Successfully loaded configuration file: {config_path}")
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Configuration file JSON format error: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Failed to load configuration file: {e}")
        exit(1)


async def main(config_path=None, skip_validation=False):
    """Run trading experiment using BaseAgent class
    
    Args:
        config_path: Configuration file path, if None use default config
        skip_validation: Skip configuration validation (not recommended)
    """
    # Determine config path
    if config_path is None:
        config_path = Path(__file__).parent / "configs" / "okx_crypto_config.json"
    else:
        config_path = Path(config_path)
    
    # Run validation unless explicitly skipped
    if not skip_validation:
        print("🔍 Validating configuration...")
        if not run_validation(str(config_path)):
            print("\n❌ Validation failed. Fix errors before proceeding.")
            print("💡 To skip validation (not recommended), use --skip-validation flag")
            exit(1)
        print("✅ Validation passed!\n")
    
    # Load configuration file
    config = load_config(config_path)
    
    # Get Agent type
    agent_type = config.get("agent_type", "BaseAgent")
    try:
        AgentClass = get_agent_class(agent_type)
    except (ValueError, ImportError, AttributeError) as e:
        print(str(e))
        exit(1)
    
    # Get date range from configuration file
    INIT_DATE = config["date_range"]["init_date"]
    END_DATE = config["date_range"]["end_date"]
    
    # Environment variables can override dates in configuration file
    if os.getenv("INIT_DATE"):
        INIT_DATE = os.getenv("INIT_DATE")
        print(f"⚠️  Using environment variable to override INIT_DATE: {INIT_DATE}")
    if os.getenv("END_DATE"):
        END_DATE = os.getenv("END_DATE")
        print(f"⚠️  Using environment variable to override END_DATE: {END_DATE}")
    
    # Validate date range
    INIT_DATE_obj = datetime.strptime(INIT_DATE, "%Y-%m-%d").date()
    END_DATE_obj = datetime.strptime(END_DATE, "%Y-%m-%d").date()
    if INIT_DATE_obj > END_DATE_obj:
        print("❌ INIT_DATE is greater than END_DATE")
        exit(1)
 
    # Get model list from configuration file (only select enabled models)
    enabled_models = [
        model for model in config["models"] 
        if model.get("enabled", True)
    ]
    
    # Get agent configuration
    agent_config = config.get("agent_config", {})
    log_config = config.get("log_config", {})
    max_steps = agent_config.get("max_steps", 10)
    max_retries = agent_config.get("max_retries", 3)
    base_delay = agent_config.get("base_delay", 0.5)
    initial_cash = agent_config.get("initial_cash", 10000.0)
    
    # Display enabled model information
    model_names = [m.get("name", m.get("signature")) for m in enabled_models]
    
    print("🚀 Starting trading experiment")
    print(f"🤖 Agent type: {agent_type}")
    print(f"📅 Date range: {INIT_DATE} to {END_DATE}")
    print(f"🤖 Model list: {model_names}")
    print(f"⚙️  Agent config: max_steps={max_steps}, max_retries={max_retries}, base_delay={base_delay}, initial_cash={initial_cash}")
                    
    for model_config in enabled_models:
        # Read basemodel and signature directly from configuration file
        model_name = model_config.get("name", "unknown")
        basemodel = model_config.get("basemodel")
        signature = model_config.get("signature")
        openai_base_url = model_config.get("openai_base_url",None)
        openai_api_key = model_config.get("openai_api_key",None)

        # Validate required fields
        if not basemodel:
            print(f"❌ Model {model_name} missing basemodel field")
            continue
        if not signature:
            print(f"❌ Model {model_name} missing signature field")
            continue
        
        print("=" * 60)
        print(f"🤖 Processing model: {model_name}")
        print(f"📝 Signature: {signature}")
        print(f"🔧 BaseModel: {basemodel}")
        
        # Initialize runtime configuration
        write_config_value("SIGNATURE", signature)
        write_config_value("TODAY_DATE", END_DATE)
        write_config_value("IF_TRADE", False)


        # Get log path configuration
        log_path = log_config.get("log_path", "./data/agent_data")

        try:
            # Dynamically create Agent instance
            agent = AgentClass(
                signature=signature,
                basemodel=basemodel,
                stock_symbols=all_crypto_symbols,
                log_path=log_path,
                openai_base_url=openai_base_url,
                openai_api_key=openai_api_key,
                max_steps=max_steps,
                max_retries=max_retries,
                base_delay=base_delay,
                initial_cash=initial_cash,
                init_date=INIT_DATE
            )
            
            print(f"✅ {agent_type} instance created successfully: {agent}")
            
            # Initialize MCP connection and AI model
            await agent.initialize()
            print("✅ Initialization successful")
            # Run all trading days in date range
            await agent.run_date_range(INIT_DATE, END_DATE)
            
            # Display final position summary
            summary = agent.get_position_summary()
            print(f"📊 Final position summary:")
            print(f"   - Latest date: {summary.get('latest_date')}")
            print(f"   - Total records: {summary.get('total_records')}")
            print(f"   - Cash balance: ${summary.get('positions', {}).get('CASH', 0):.2f}")
            
        except Exception as e:
            print(f"❌ Error processing model {model_name} ({signature}): {str(e)}")
            print(f"📋 Error details: {e}")
            # Can choose to continue processing next model, or exit
            # continue  # Continue processing next model
            exit()  # Or exit program
        
        print("=" * 60)
        print(f"✅ Model {model_name} ({signature}) processing completed")
        print("=" * 60)
    
    print("🎉 All models processing completed!")
    
if __name__ == "__main__":
    import sys
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI-Trader: AI-driven cryptocurrency trading system')
    parser.add_argument('config', nargs='?', default=None, help='Configuration file path')
    parser.add_argument('--skip-validation', action='store_true', help='Skip configuration validation (not recommended)')
    parser.add_argument('--validate-only', action='store_true', help='Only run validation, do not start trading')
    
    args = parser.parse_args()
    
    config_path = args.config
    
    if args.validate_only:
        # Run validation only
        print("🔍 Running configuration validation only...\n")
        config_to_validate = config_path or "configs/okx_crypto_config.json"
        if run_validation(config_to_validate):
            print("✅ Configuration is valid!")
            sys.exit(0)
        else:
            print("❌ Configuration validation failed!")
            sys.exit(1)
    
    # Normal operation
    if config_path:
        print(f"📄 Using specified configuration file: {config_path}")
    else:
        print(f"📄 Using default configuration file: configs/okx_crypto_config.json")
    
    asyncio.run(main(config_path, skip_validation=args.skip_validation))

