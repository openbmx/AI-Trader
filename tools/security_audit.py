"""
Security Audit and Best Practices Check
Scans the codebase for potential security issues
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple


class SecurityIssue:
    """Represents a security issue found during audit"""
    
    SEVERITY_CRITICAL = "CRITICAL"
    SEVERITY_HIGH = "HIGH"
    SEVERITY_MEDIUM = "MEDIUM"
    SEVERITY_LOW = "LOW"
    SEVERITY_INFO = "INFO"
    
    def __init__(self, severity: str, file: str, line: int, issue: str, recommendation: str):
        self.severity = severity
        self.file = file
        self.line = line
        self.issue = issue
        self.recommendation = recommendation
    
    def __repr__(self):
        return f"[{self.severity}] {self.file}:{self.line} - {self.issue}"


class SecurityAuditor:
    """Performs security audit on the codebase"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.issues: List[SecurityIssue] = []
    
    def audit_file(self, file_path: Path) -> List[SecurityIssue]:
        """
        Audit a single file for security issues
        
        Args:
            file_path: Path to the file to audit
            
        Returns:
            List of security issues found
        """
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            return issues
        
        for line_num, line in enumerate(lines, 1):
            # Check for hardcoded secrets
            if self._check_hardcoded_secrets(line):
                issues.append(SecurityIssue(
                    SecurityIssue.SEVERITY_CRITICAL,
                    str(file_path),
                    line_num,
                    "Potential hardcoded API key or secret detected",
                    "Use environment variables instead of hardcoding secrets"
                ))
            
            # Check for SQL injection vulnerabilities (if using SQL)
            if self._check_sql_injection(line):
                issues.append(SecurityIssue(
                    SecurityIssue.SEVERITY_HIGH,
                    str(file_path),
                    line_num,
                    "Potential SQL injection vulnerability",
                    "Use parameterized queries instead of string concatenation"
                ))
            
            # Check for eval() usage
            if self._check_eval_usage(line):
                issues.append(SecurityIssue(
                    SecurityIssue.SEVERITY_HIGH,
                    str(file_path),
                    line_num,
                    "Use of eval() detected - potential code injection risk",
                    "Avoid using eval(). Use safer alternatives like ast.literal_eval()"
                ))
            
            # Check for pickle usage
            if self._check_pickle_usage(line):
                issues.append(SecurityIssue(
                    SecurityIssue.SEVERITY_MEDIUM,
                    str(file_path),
                    line_num,
                    "Use of pickle detected - can execute arbitrary code",
                    "Consider using json or other safer serialization formats"
                ))
            
            # Check for shell=True in subprocess
            if self._check_shell_true(line):
                issues.append(SecurityIssue(
                    SecurityIssue.SEVERITY_HIGH,
                    str(file_path),
                    line_num,
                    "subprocess with shell=True - potential command injection",
                    "Avoid shell=True or sanitize all inputs carefully"
                ))
            
            # Check for insecure random number generation
            if self._check_insecure_random(line):
                issues.append(SecurityIssue(
                    SecurityIssue.SEVERITY_MEDIUM,
                    str(file_path),
                    line_num,
                    "Using random module for security-sensitive operations",
                    "Use secrets module for cryptographic purposes"
                ))
        
        return issues
    
    def _check_hardcoded_secrets(self, line: str) -> bool:
        """Check for hardcoded API keys or secrets"""
        # Skip comments
        if line.strip().startswith('#'):
            return False
        
        # Lowercase once for efficiency
        line_lower = line.lower()
        
        # Common patterns for API keys
        patterns = [
            r'["\']sk-[a-zA-Z0-9]{20,}["\']',  # OpenAI style keys
            r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'secret\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'password\s*=\s*["\'][^"\']{8,}["\']',
            r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
        ]
        
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Exclude obvious placeholders
                if any(placeholder in line_lower for placeholder in 
                       ['your_', 'example', 'placeholder', 'dummy', 'test_key', 'fake']):
                    continue
                return True
        
        return False
    
    def _check_sql_injection(self, line: str) -> bool:
        """Check for potential SQL injection vulnerabilities"""
        # Look for string concatenation in SQL-like statements
        if any(sql_keyword in line.upper() for sql_keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
            if '+' in line or '%' in line or 'format(' in line or 'f"' in line or "f'" in line:
                return True
        return False
    
    def _check_eval_usage(self, line: str) -> bool:
        """Check for eval() usage"""
        return re.search(r'\beval\s*\(', line) is not None
    
    def _check_pickle_usage(self, line: str) -> bool:
        """Check for pickle usage"""
        return 'pickle.load' in line or 'pickle.loads' in line
    
    def _check_shell_true(self, line: str) -> bool:
        """Check for subprocess with shell=True"""
        return 'subprocess' in line and 'shell=True' in line
    
    def _check_insecure_random(self, line: str) -> bool:
        """Check for insecure random number generation"""
        # Only flag if used in security context
        if 'random.' in line and not 'secrets.' in line:
            # Lowercase once for efficiency
            line_lower = line.lower()
            security_keywords = ['key', 'token', 'password', 'secret', 'salt', 'nonce']
            return any(keyword in line_lower for keyword in security_keywords)
        return False
    
    def audit_project(self) -> Dict[str, List[SecurityIssue]]:
        """
        Audit the entire project
        
        Returns:
            Dictionary mapping file paths to lists of issues
        """
        results = {}
        
        # Find all Python files
        for py_file in self.project_root.rglob("*.py"):
            # Skip virtual environments and build directories
            if any(skip in str(py_file) for skip in ['venv', 'env', '__pycache__', '.git', 'dist', 'build']):
                continue
            
            issues = self.audit_file(py_file)
            if issues:
                results[str(py_file)] = issues
                self.issues.extend(issues)
        
        return results
    
    def check_file_permissions(self) -> List[SecurityIssue]:
        """Check file permissions for sensitive files"""
        issues = []
        
        sensitive_files = ['.env', 'runtime_env.json', '.runtime_env.json']
        
        for filename in sensitive_files:
            file_path = self.project_root / filename
            if file_path.exists():
                try:
                    stat_info = file_path.stat()
                    # Extract permissions more explicitly
                    perms = oct(stat_info.st_mode & 0o777)
                    # Check if file is readable by group or others
                    if stat_info.st_mode & 0o077:
                        issues.append(SecurityIssue(
                            SecurityIssue.SEVERITY_HIGH,
                            str(file_path),
                            0,
                            f"Insecure file permissions: {perms}",
                            f"Run: chmod 600 {filename}"
                        ))
                except Exception:
                    pass
        
        return issues
    
    def generate_report(self) -> str:
        """Generate a security audit report"""
        report = []
        report.append("=" * 70)
        report.append("🔒 Security Audit Report")
        report.append("=" * 70)
        report.append("")
        
        # Count by severity
        severity_counts = {
            SecurityIssue.SEVERITY_CRITICAL: 0,
            SecurityIssue.SEVERITY_HIGH: 0,
            SecurityIssue.SEVERITY_MEDIUM: 0,
            SecurityIssue.SEVERITY_LOW: 0,
            SecurityIssue.SEVERITY_INFO: 0,
        }
        
        for issue in self.issues:
            severity_counts[issue.severity] += 1
        
        # Summary
        report.append("📊 Summary:")
        report.append(f"   Total Issues: {len(self.issues)}")
        for severity, count in severity_counts.items():
            if count > 0:
                emoji = "🔴" if severity == SecurityIssue.SEVERITY_CRITICAL else \
                        "🟠" if severity == SecurityIssue.SEVERITY_HIGH else \
                        "🟡" if severity == SecurityIssue.SEVERITY_MEDIUM else \
                        "🟢"
                report.append(f"   {emoji} {severity}: {count}")
        report.append("")
        
        # Group issues by file
        issues_by_file = {}
        for issue in self.issues:
            if issue.file not in issues_by_file:
                issues_by_file[issue.file] = []
            issues_by_file[issue.file].append(issue)
        
        # Detailed issues
        if self.issues:
            report.append("📋 Detailed Issues:")
            report.append("")
            
            for file_path, issues in sorted(issues_by_file.items()):
                report.append(f"File: {file_path}")
                for issue in issues:
                    report.append(f"  Line {issue.line}: [{issue.severity}]")
                    report.append(f"    Issue: {issue.issue}")
                    report.append(f"    Fix: {issue.recommendation}")
                    report.append("")
        else:
            report.append("✅ No security issues found!")
            report.append("")
        
        # Recommendations
        report.append("=" * 70)
        report.append("💡 General Security Recommendations:")
        report.append("=" * 70)
        report.append("")
        report.append("1. ✅ Always use environment variables for secrets")
        report.append("2. ✅ Keep dependencies up to date")
        report.append("3. ✅ Use HTTPS for all API calls")
        report.append("4. ✅ Implement rate limiting")
        report.append("5. ✅ Enable OKX API IP whitelist")
        report.append("6. ✅ Never commit .env files")
        report.append("7. ✅ Rotate API keys regularly")
        report.append("8. ✅ Test on testnet before production")
        report.append("9. ✅ Monitor for unusual activity")
        report.append("10. ✅ Set file permissions correctly (chmod 600 .env)")
        report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


def run_security_audit(project_root: str = ".") -> Tuple[bool, str]:
    """
    Run security audit and return results
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        Tuple of (passed, report)
    """
    auditor = SecurityAuditor(project_root)
    
    # Audit code
    auditor.audit_project()
    
    # Check file permissions
    permission_issues = auditor.check_file_permissions()
    auditor.issues.extend(permission_issues)
    
    # Generate report
    report = auditor.generate_report()
    
    # Consider critical and high severity issues as failures
    critical_or_high = sum(1 for issue in auditor.issues 
                          if issue.severity in [SecurityIssue.SEVERITY_CRITICAL, 
                                               SecurityIssue.SEVERITY_HIGH])
    
    passed = critical_or_high == 0
    
    return passed, report


if __name__ == "__main__":
    """Run security audit when executed directly"""
    import sys
    
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print(f"🔍 Running security audit on: {project_root}\n")
    
    passed, report = run_security_audit(project_root)
    
    print(report)
    
    if passed:
        print("✅ Security audit passed!")
        sys.exit(0)
    else:
        print("⚠️  Security audit found critical or high severity issues.")
        print("Please review and fix them before deploying to production.")
        sys.exit(1)
