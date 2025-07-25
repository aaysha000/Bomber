🖥️ SmartBrowserBomb

Behaviour‑triggered proof‑of‑concept malware written in Python.  
It spams browser tabs, grabs a webcam snapshot, and logs everything - with both GUI and headless modes.

<img width="975" height="767" alt="image" src="https://github.com/user-attachments/assets/d9b019c6-4195-4a63-9040-ae3afed047f4" />

⚠️ Disclaimer
Educational / demo purposes only. Running malware on systems you don’t own or have explicit permission to test is illegal.


✨ Features
- Tkinter GUI controller & status display
- Process‑aware trigger (launches when a new user process starts)
- DoS‑like tab flood via `webbrowser` module
- Webcam capture with OpenCV
- Headless mode (`HEADLESS_MODE=True`) for silent runs
- Detailed logging to `activity.log`


🔧 Installation & Usage
  
Install Required Dependencies

Run:
pip install -r requirements.txt
