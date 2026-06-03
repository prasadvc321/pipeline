import os
import re

from agent_guard import fail

print("Running Security Agent...")

secret_patterns = {
    "Password": r"(?i)\bpassword\b\s*[:=]\s*['\"][^'\"]{4,}['\"]",
    "Secret": r"(?i)\bsecret\b\s*[:=]\s*['\"][^'\"]{8,}['\"]",
    "Token": r"(?i)\btoken\b\s*[:=]\s*['\"][^'\"]{8,}['\"]",
    "API Key": r"(?i)\bapi[_-]?key\b\s*[:=]\s*['\"][^'\"]{8,}['\"]",
    "Email": r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b",
}

scan_extensions = {".py", ".html", ".css", ".js", ".json", ".yml", ".yaml", ".env"}
skip_dirs = {".git", "__pycache__", ".venv", "venv", ".github", "node_modules"}

issues = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in skip_dirs]

    for file_name in files:
        _, extension = os.path.splitext(file_name)

        if extension not in scan_extensions:
            continue

        path = os.path.join(root, file_name)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):

                for name, pattern in secret_patterns.items():
                    match = re.search(pattern, line)

                    if match:
                        issues.append({
                            "file": path,
                            "line": line_no,
                            "type": name,
                            "content": line.strip()
                        })

if issues:
    print("\nPossible hard-coded secrets found:\n")

    for issue in issues:
        print(
            f"{issue['file']}:{issue['line']} "
            f"[{issue['type']}]"
        )
        print(f"    {issue['content']}")
        print()

    fail("Security Agent found blocking condition(s).")

print("Security scan passed.")
