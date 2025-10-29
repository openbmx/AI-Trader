# Scripts Directory

This directory contains utility scripts for the AI-Trader system.

## Available Scripts

### pre_deployment_check.sh

Comprehensive pre-deployment checklist and validation script.

**Usage:**
```bash
./scripts/pre_deployment_check.sh
```

**What it checks:**
1. Python version (3.8+)
2. Required files exist
3. File permissions (security)
4. Python dependencies installed
5. Environment variables configured
6. Configuration validation
7. Disk space available
8. Network connectivity to APIs
9. Security audit

**When to use:**
- Before deploying to production
- After making configuration changes
- When troubleshooting issues
- As part of CI/CD pipeline

## Adding New Scripts

When adding new scripts:
1. Make them executable: `chmod +x script_name.sh`
2. Add documentation to this README
3. Follow the existing style and error handling
4. Include helpful error messages
