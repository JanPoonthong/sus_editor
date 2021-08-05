"""DO NOT RUN IT FILE ON LOCAL MACHINE"""
import subprocess

subprocess.Popen("python3 main.py", shell=True)
from pynput.mouse import Button, Controller
import time

mouse = Controller()
subprocess.Popen("xkill", shell=True)
mouse.position = (200, 400)
time.sleep(0.50)
mouse.click(Button.left, 1)
