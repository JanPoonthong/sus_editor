"""DO NOT RUN IT FILE ON LOCAL MACHINE"""
import subprocess
import time

xvfb = subprocess.Popen(
    'export DISPLAY=:1 && Xvfb "${DISPLAY}" -screen 0 1024x768x24', shell=True
)
time.sleep(1)
ci = subprocess.Popen("export DISPLAY=:1 && python3 ci.py", shell=True)
ci.wait()
subprocess.Popen("killall Xvfb", shell=True)
