import subprocess
import time
subprocess.Popen('export DISPLAY=:1 && Xvfb "${DISPLAY}" -screen 0 1024x768x24', shell=True)
time.sleep(1)
subprocess.Popen('export DISPLAY=:1 && python3 ci.py', shell=True)
time.sleep(1)
subprocess.Popen('killall Xvfb', shell=True)
