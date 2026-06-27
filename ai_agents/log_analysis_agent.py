```python
import os
import re

from agent_guard import fail, fail_if_matches
from ai_provider import ask_ai

print("Running AI Log Analysis Agent...")

# -------------------------------------------------------
# Collect logs from multiple sources
# -------------------------------------------------------
logs = ""

log_files = [
    "output.log",
    "error.log"
]

for logfile in log_files:
    if os.path.exists(logfile):
        with open(logfile, "r", encoding="utf-8", errors="ignore") as f:
            logs += f"\n\n===== {logfile} =====\n"
            logs += f.read()

if not logs.strip():
    fail("No logs found for AI analysis.")

recent_logs = logs[-5000:]

# -------------------------------------------------------
# Deterministic runtime failure detection
# -------------------------------------------------------
log_blocking_patterns = [
    r"traceback",
    r"modulenotfounderror",
    r"importerror",
    r"syntaxerror",
    r"segmentation fault",
    r"permission denied",
    r"address already in use",
    r"connection refused",
    r"startup failed",
    r"failed to bind",
    r"fatal runtime error",
]

fail_if_matches(
    "Runtime Log Gate",
    recent_logs.lower(),
    log_blocking_patterns
)

# -------------------------------------------------------
# AI Root Cause Analysis
# -------------------------------------------------------
prompt = f"""
Analyze the following application logs.

Provide:

- Errors
- Warnings
- Root Cause
- Deployment Issues
- Recommended Fix

Decision Rules:

Return PIPELINE_STATUS: FAIL only if:
- Application crashed
- Unhandled exception occurred
- Startup failed
- Server failed to start
- Port binding failed
- Requests cannot be served

Return PIPELINE_STATUS: PASS if:
- Application started successfully
- Only warnings are present
- Deprecation warnings exist
- FutureWarnings exist

Return exactly in the following format:

Errors:
...

Warnings:
...

Root Cause:
...

Deployment Issues:
...

Recommended Fix:
...

PIPELINE_STATUS: PASS
or
PIPELINE_STATUS: FAIL

Logs:
{recent_logs}
"""

response = ask_ai(prompt)

print(response)

# -------------------------------------------------------
# Validate AI response format
# -------------------------------------------------------
status_match = re.search(
    r"PIPELINE_STATUS:\s*(PASS|FAIL)",
    response,
    re.IGNORECASE
)

if not status_match:
    fail("AI response missing PIPELINE_STATUS.")

pipeline_status = status_match.group(1).upper()

if pipeline_status == "FAIL":
    fail(
        "AI Log Analysis Agent detected deployment failure."
    )

# -------------------------------------------------------
# Additional AI safety patterns
# -------------------------------------------------------
ai_blocking_patterns = [
    r"deployment should not proceed",
    r"do not deploy",
    r"fatal runtime error",
    r"startup failed",
    r"application crash",
]

fail_if_matches(
    "AI Log Analysis Agent",
    response.lower(),
    ai_blocking_patterns
)

print("AI Log Analysis Agent gate passed.")
```
