#!/bin/bash
# Pre-deployment checklist and validation script

set -e

echo "========================================================================"
echo "🚀 AI-Trader Pre-Deployment Checklist"
echo "========================================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ALL_CHECKS_PASSED=true

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        ALL_CHECKS_PASSED=false
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "1️⃣  Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -ge 3 ] && [ "$python_minor" -ge 8 ]; then
    print_status 0 "Python version $python_version"
else
    print_status 1 "Python version $python_version (requires 3.8+)"
fi
echo ""

echo "2️⃣  Checking required files..."
required_files=(".env" "requirements.txt" "main.py" "configs/okx_crypto_config.json")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "File exists: $file"
    else
        print_status 1 "File missing: $file"
    fi
done
echo ""

echo "3️⃣  Checking file permissions..."
if [ -f ".env" ]; then
    perm=$(stat -c %a .env 2>/dev/null || stat -f %A .env 2>/dev/null)
    if [ "$perm" = "600" ]; then
        print_status 0 ".env permissions: $perm"
    else
        print_status 1 ".env permissions: $perm (should be 600)"
        echo "   Run: chmod 600 .env"
    fi
fi

if [ -f ".runtime_env.json" ]; then
    perm=$(stat -c %a .runtime_env.json 2>/dev/null || stat -f %A .runtime_env.json 2>/dev/null)
    if [ "$perm" = "600" ]; then
        print_status 0 ".runtime_env.json permissions: $perm"
    else
        print_status 1 ".runtime_env.json permissions: $perm (should be 600)"
        echo "   Run: chmod 600 .runtime_env.json"
    fi
fi
echo ""

echo "4️⃣  Checking Python dependencies..."
if python -c "import langchain" 2>/dev/null; then
    print_status 0 "langchain installed"
else
    print_status 1 "langchain not installed"
    echo "   Run: pip install -r requirements.txt"
fi

if python -c "import ccxt" 2>/dev/null; then
    print_status 0 "ccxt installed"
else
    print_status 1 "ccxt not installed"
    echo "   Run: pip install -r requirements.txt"
fi
echo ""

echo "5️⃣  Checking environment variables..."
if [ -f ".env" ]; then
    source .env 2>/dev/null || true
    
    # Check OKX variables
    if [ -n "$OKX_API_KEY" ] && [ "$OKX_API_KEY" != "your_okx_api_key_here" ]; then
        print_status 0 "OKX_API_KEY is set"
    else
        print_status 1 "OKX_API_KEY not configured"
    fi
    
    if [ -n "$OKX_API_SECRET" ] && [ "$OKX_API_SECRET" != "your_okx_api_secret_here" ]; then
        print_status 0 "OKX_API_SECRET is set"
    else
        print_status 1 "OKX_API_SECRET not configured"
    fi
    
    if [ -n "$OKX_PASSPHRASE" ] && [ "$OKX_PASSPHRASE" != "your_okx_passphrase_here" ]; then
        print_status 0 "OKX_PASSPHRASE is set"
    else
        print_status 1 "OKX_PASSPHRASE not configured"
    fi
    
    # Check testnet setting
    if [ "$OKX_TESTNET" = "true" ]; then
        print_status 0 "OKX_TESTNET=true (safe)"
    elif [ "$OKX_TESTNET" = "false" ]; then
        print_warning "OKX_TESTNET=false - REAL MONEY TRADING!"
    else
        print_status 1 "OKX_TESTNET not set"
    fi
    
    # Check AI API key (at least one should be configured)
    ai_configured=false
    if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your_openai_api_key_here" ]; then
        print_status 0 "OPENAI_API_KEY is set"
        ai_configured=true
    fi
    
    if [ -n "$DEEPSEEK_API_KEY" ] && [ "$DEEPSEEK_API_KEY" != "your_deepseek_api_key_here" ]; then
        print_status 0 "DEEPSEEK_API_KEY is set"
        ai_configured=true
    fi
    
    if [ -n "$ANTHROPIC_API_KEY" ] && [ "$ANTHROPIC_API_KEY" != "your_anthropic_api_key_here" ]; then
        print_status 0 "ANTHROPIC_API_KEY is set"
        ai_configured=true
    fi
    
    if [ "$ai_configured" = false ]; then
        print_status 1 "No AI API key configured"
    fi
else
    print_status 1 ".env file not found"
fi
echo ""

echo "6️⃣  Running configuration validation..."
if python tools/config_validator.py configs/okx_crypto_config.json > /tmp/validation.log 2>&1; then
    print_status 0 "Configuration validation passed"
else
    print_status 1 "Configuration validation failed"
    echo "   See details: cat /tmp/validation.log"
fi
echo ""

echo "7️⃣  Checking disk space..."
available_space=$(df -h . | awk 'NR==2 {print $4}')
print_status 0 "Available disk space: $available_space"
echo ""

echo "8️⃣  Checking network connectivity..."
if curl -s --max-time 5 https://www.okx.com > /dev/null; then
    print_status 0 "Can reach OKX (okx.com)"
else
    print_status 1 "Cannot reach OKX"
fi

if curl -s --max-time 5 https://api.openai.com > /dev/null; then
    print_status 0 "Can reach OpenAI (api.openai.com)"
else
    print_warning "Cannot reach OpenAI (may not be needed)"
fi
echo ""

echo "9️⃣  Running security audit..."
if python tools/security_audit.py . > /tmp/security.log 2>&1; then
    print_status 0 "Security audit passed"
else
    print_warning "Security audit found issues (see /tmp/security.log)"
fi
echo ""

echo "========================================================================"
if [ "$ALL_CHECKS_PASSED" = true ]; then
    echo -e "${GREEN}✅ All critical checks passed!${NC}"
    echo ""
    echo "Ready to deploy! 🚀"
    echo ""
    echo "Next steps:"
    echo "  1. Review your configuration one more time"
    echo "  2. If using real money, double-check OKX_TESTNET=false"
    echo "  3. Start with small amounts"
    echo "  4. Monitor the system closely"
    echo ""
    echo "To start the system, run:"
    echo "  ./main.sh"
    echo "  or"
    echo "  python main.py"
else
    echo -e "${RED}❌ Some checks failed!${NC}"
    echo ""
    echo "Please fix the issues above before deploying."
    echo ""
    echo "For help, see:"
    echo "  - docs/PRODUCTION_GUIDE.md"
    echo "  - docs/AI_PROVIDERS_GUIDE.md"
    echo "  - DEPLOYMENT.md"
fi
echo "========================================================================"

# Exit with appropriate code
if [ "$ALL_CHECKS_PASSED" = true ]; then
    exit 0
else
    exit 1
fi
