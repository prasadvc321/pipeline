import os
import re

from agent_guard import fail, fail_if_matches
from ai_provider import ask_ai

print("Running AI Log Analysis Agent...")

if not os.path.exists("output.log"):
    fail("output.log not found.")

with open("output.log", "r", encoding="utf-8", errors="ignore") as f:
    logs = f.read()

recent_logs = logs[-3000:]

# Block only on real runtime failures
log_blocking_patterns = [
    r"\btraceback\b",
    r"\bexception\b",
    r"\berror\b",
    r"\bfailed\b",
    r"\bcrash\b",
    r"\baddress already in use\b",
]

fail_if_matches("Runtime Log Gate", recent_logs, log_blocking_patterns)

prompt = f"""
Analyze the following Flask application logs.

Report:
- Errors
- Warnings
- Crash reasons
- Deployment issues

Decision Rules:
1. Return PIPELINE_STATUS: FAIL ONLY if the logs show:
   - Application crash
   - Unhandled exception
   - Startup failure
   - Port binding failure
   - Server failed to start
   - Fatal runtime error
   - Requests cannot be served

2. Return PIPELINE_STATUS: PASS if:
   - The application starts successfully.
   - Only warnings are present.
   - Flask development server warning is shown.
   - Debug mode is enabled.
   - Deprecation/FutureWarning messages are present.

Important:
- Flask's "development server" warning is NOT a deployment failure.
- Debug mode enabled is a warning, NOT a failure.
- Python deprecation warnings are NOT failures.
- FutureWarning messages are NOT failures.

Return in this format:

Errors:
...

Warnings:
...

Crash Reasons:
...

Deployment Issues:
...

PIPELINE_STATUS: PASS
or
PIPELINE_STATUS: FAIL

Logs:
{recent_logs}
"""

response = ask_ai(prompt)

print(response)

# Fail only if AI detects an actual runtime/deployment blocker
if re.search(r"PIPELINE_STATUS:\s*FAIL", response, re.IGNORECASE):
    fail("AI Log Analysis Agent reported a runtime/deployment failure.")

# Extra safety checks
ai_blocking_patterns = [
    r"\bdeployment should not proceed\b",
    r"\bdo not deploy\b",
    r"\bfatal runtime error\b",
    r"\bstartup failed\b",
]

fail_if_matches("AI Log Analysis Agent", response, ai_blocking_patterns)

print("AI Log Analysis Agent gate passed.")
