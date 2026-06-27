# Ai log analysis agent flow 

Start
   │
   ▼
Check output.log exists
   │
   ▼
Read latest logs
   │
   ▼
Search for critical runtime errors
   │
   ├── Error found → FAIL
   │
   ▼
Send logs to Gemini AI
   │
   ▼
AI identifies:
   • Errors
   • Warnings
   • Crash reasons
   • Deployment issues
   │
   ▼
AI returns PASS or FAIL
   │
   ▼
Optional AI phrase checks
   │
   ├── Blocking phrase found → FAIL
   │
   ▼
Pipeline passes


