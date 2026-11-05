WEBGUARD - FIXED DEMO
=====================

FIXES INCLUDED
1. Flask homepage template is now in templates/index.html, where Flask expects it.
2. Added the missing Secure site :8002 button (the JavaScript already expected id="la").
3. Improved JSON validation and report generation error handling.
4. Updated run_demo.bat to start the practice lab and Flask server before opening the browser.

HOW TO RUN
1. Extract this ZIP into a new folder, for example Desktop\WebGuard_Fixed.
2. Make sure Python is installed and available as the `python` command.
3. Double-click run_demo.bat.
4. Keep both command windows open.
5. Open http://127.0.0.1:5000 if it does not open automatically.
6. Tick the permission checkbox before running a scan.
7. For the local lab, use Local Practice mode and scan http://127.0.0.1:8001 or click the local lab buttons.

IMPORTANT
- This is an educational, passive security-header assessment, not a penetration test.
- Only scan websites you own or have explicit permission to assess.
- Do not upload .env files, passwords, API keys, or other secrets.
