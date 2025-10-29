"""
Configuration and Environment Validation Module
Validates system configuration before running in production
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class ConfigValidator:
    """Validates configuration and environment settings"""
    
    # Required environment variables for different providers
    REQUIRED_ENV_VARS = {
        "openai": ["OPENAI_API_KEY"],
        "ollama": [],  # No API key required
        "deepseek": ["DEEPSEEK_API_KEY"],
        "anthropic": ["ANTHROPIC_API_KEY"],
        "github_copilot": ["GITHUB_COPILOT_API_KEY"],
        "google_gemini": ["GOOGLE_GEMINI_API_KEY"],
    }
    
    # OKX related required variables
    OKX_REQUIRED = ["OKX_API_KEY", "OKX_API_SECRET", "OKX_PASSPHRASE"]
    
    @staticmethod
    def validate_env_file() -> Tuple[bool, List[str]]:
        """
        Validate .env file exists and is readable
        
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        env_path = Path(".env")
        if not env_path.exists():
            errors.append("⚠️  .env file not found. Copy .env.example to .env and configure it.")
            return False, errors
        
        # Check file permissions (Unix-like systems)
        if hasattr(os, 'stat'):
            stat_info = env_path.stat()
            if stat_info.st_mode & 0o077:  # Check if group or others have any permission
                errors.append("⚠️  .env file has insecure permissions. Run: chmod 600 .env")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_api_keys(provider: str) -> Tuple[bool, List[str]]:
        """
        Validate API keys for a specific provider
        
        Args:
            provider: Provider name (e.g., 'openai', 'ollama')
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        warnings = []
        
        provider = provider.lower()
        required_vars = ConfigValidator.REQUIRED_ENV_VARS.get(provider, [])
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                errors.append(f"❌ Missing required environment variable: {var}")
            elif value.startswith("your_") or value == "":
                errors.append(f"❌ {var} appears to be a placeholder. Please set a real value.")
        
        # Check base URL
        base_url_var = f"{provider.upper()}_API_BASE"
        base_url = os.getenv(base_url_var) or os.getenv("OPENAI_API_BASE")
        if not base_url and provider not in ["ollama"]:
            warnings.append(f"⚠️  {base_url_var} not set, using default")
        
        return len(errors) == 0, errors + warnings
    
    @staticmethod
    def validate_okx_config() -> Tuple[bool, List[str]]:
        """
        Validate OKX exchange configuration
        
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        warnings = []
        
        # Check required variables
        for var in ConfigValidator.OKX_REQUIRED:
            value = os.getenv(var)
            if not value:
                errors.append(f"❌ Missing required OKX variable: {var}")
            elif value.startswith("your_"):
                errors.append(f"❌ {var} appears to be a placeholder")
        
        # Check testnet setting
        testnet = os.getenv("OKX_TESTNET", "true").lower()
        if testnet not in ["true", "false"]:
            errors.append(f"❌ OKX_TESTNET must be 'true' or 'false', got: {testnet}")
        elif testnet == "false":
            warnings.append("⚠️  OKX_TESTNET is false - REAL MONEY TRADING ENABLED!")
            warnings.append("⚠️  Make sure you understand the risks before proceeding.")
        
        return len(errors) == 0, errors + warnings
    
    @staticmethod
    def validate_config_file(config_path: str) -> Tuple[bool, List[str]]:
        """
        Validate configuration file structure
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        path = Path(config_path)
        if not path.exists():
            errors.append(f"❌ Configuration file not found: {config_path}")
            return False, errors
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"❌ Invalid JSON in configuration file: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"❌ Error reading configuration file: {e}")
            return False, errors
        
        # Validate required fields
        required_fields = ["agent_type", "date_range", "models", "agent_config"]
        for field in required_fields:
            if field not in config:
                errors.append(f"❌ Missing required field in config: {field}")
        
        # Validate date_range
        if "date_range" in config:
            date_range = config["date_range"]
            if "init_date" not in date_range or "end_date" not in date_range:
                errors.append("❌ date_range must have init_date and end_date")
        
        # Validate models
        if "models" in config:
            models = config["models"]
            if not isinstance(models, list) or len(models) == 0:
                errors.append("❌ models must be a non-empty array")
            else:
                enabled_models = [m for m in models if m.get("enabled", True)]
                if len(enabled_models) == 0:
                    errors.append("❌ No enabled models found in configuration")
                
                for i, model in enumerate(models):
                    if "basemodel" not in model:
                        errors.append(f"❌ Model {i} missing 'basemodel' field")
                    if "signature" not in model:
                        errors.append(f"❌ Model {i} missing 'signature' field")
        
        # Validate agent_config
        if "agent_config" in config:
            agent_config = config["agent_config"]
            if "max_steps" in agent_config:
                max_steps = agent_config["max_steps"]
                if not isinstance(max_steps, int) or max_steps < 1:
                    errors.append("❌ max_steps must be a positive integer")
            
            if "initial_cash" in agent_config:
                initial_cash = agent_config["initial_cash"]
                if not isinstance(initial_cash, (int, float)) or initial_cash <= 0:
                    errors.append("❌ initial_cash must be a positive number")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_system_resources() -> Tuple[bool, List[str]]:
        """
        Validate system resources
        
        Returns:
            Tuple of (is_valid, warnings)
        """
        warnings = []
        
        try:
            import shutil
            
            # Check disk space
            disk_usage = shutil.disk_usage(".")
            free_gb = disk_usage.free / (1024 ** 3)
            if free_gb < 1:
                warnings.append(f"⚠️  Low disk space: {free_gb:.2f} GB free")
            
            # Check Python version
            if sys.version_info < (3, 8):
                warnings.append(f"⚠️  Python version {sys.version_info.major}.{sys.version_info.minor} is below recommended 3.8+")
        
        except Exception as e:
            warnings.append(f"⚠️  Could not check system resources: {e}")
        
        return True, warnings
    
    @staticmethod
    def validate_all(config_path: Optional[str] = None) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Run all validations
        
        Args:
            config_path: Optional path to configuration file
            
        Returns:
            Tuple of (is_valid, results_dict)
        """
        results = {}
        all_valid = True
        
        # Validate .env file
        valid, messages = ConfigValidator.validate_env_file()
        results["env_file"] = messages
        all_valid = all_valid and valid
        
        # Validate OKX configuration
        valid, messages = ConfigValidator.validate_okx_config()
        results["okx_config"] = messages
        all_valid = all_valid and valid
        
        # Validate configuration file if provided
        if config_path:
            valid, messages = ConfigValidator.validate_config_file(config_path)
            results["config_file"] = messages
            all_valid = all_valid and valid
        
        # Validate system resources
        valid, messages = ConfigValidator.validate_system_resources()
        results["system_resources"] = messages
        # Don't fail on resource warnings
        
        return all_valid, results
    
    @staticmethod
    def print_validation_results(results: Dict[str, List[str]]) -> None:
        """
        Print validation results in a readable format
        
        Args:
            results: Dictionary of validation results
        """
        print("\n" + "=" * 60)
        print("🔍 Configuration Validation Results")
        print("=" * 60 + "\n")
        
        has_errors = False
        has_warnings = False
        
        for category, messages in results.items():
            if messages:
                print(f"📋 {category.replace('_', ' ').title()}:")
                for msg in messages:
                    print(f"   {msg}")
                    if "❌" in msg:
                        has_errors = True
                    elif "⚠️" in msg:
                        has_warnings = True
                print()
        
        if not has_errors and not has_warnings:
            print("✅ All validations passed!")
        elif has_errors:
            print("❌ Validation failed! Please fix the errors above.")
        else:
            print("⚠️  Validation passed with warnings. Review them before proceeding.")
        
        print("=" * 60 + "\n")


def run_validation(config_path: Optional[str] = None) -> bool:
    """
    Run validation and print results
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        True if validation passed, False otherwise
    """
    is_valid, results = ConfigValidator.validate_all(config_path)
    ConfigValidator.print_validation_results(results)
    return is_valid


if __name__ == "__main__":
    """Run validation when executed directly"""
    import sys
    
    config_path = sys.argv[1] if len(sys.argv) > 1 else "configs/okx_crypto_config.json"
    
    print(f"🔍 Validating configuration: {config_path}\n")
    
    if run_validation(config_path):
        print("✅ Ready to run!")
        sys.exit(0)
    else:
        print("❌ Please fix the errors before running.")
        sys.exit(1)
