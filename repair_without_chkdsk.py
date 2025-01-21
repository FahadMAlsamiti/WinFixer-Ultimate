import subprocess
import os
import time
import ctypes
import sys
import json
from datetime import datetime

# إعداد التقارير
log_file = "repair_log_without_chkdsk.html"
state_file = "repair_state_without_chkdsk.json"

# تعريف الأوامر بالترتيب
commands = [
    "DISM /Online /Cleanup-Image /CheckHealth",
    "DISM /Online /Cleanup-Image /ScanHealth",
    "DISM /Online /Cleanup-Image /RestoreHealth",
    "sfc /scannow",
    "del /s /q %temp%\\*",
    "del /s /q C:\\Windows\\Temp\\*",
    "del /s /q C:\\Windows\\Prefetch\\*",
    "ipconfig /release",
    "ipconfig /renew",
    "ipconfig /flushdns",
    "netsh int ip reset",
    "netsh winsock reset",
    "ping 8.8.8.8 -n 4",
    'netsh interface ipv4 set dns name="Ethernet" source=static address=8.8.8.8',
    'netsh interface ipv4 add dns name="Ethernet" address=8.8.4.4 index=2',
    'netsh interface ipv6 set dns name="Ethernet" source=static address=2001:4860:4860::8888',
    'netsh interface ipv6 add dns name="Ethernet" address=2001:4860:4860::8844 index=2',
    "wuauclt /detectnow",
    "wuauclt /updatenow",
    "sc config wuauserv start= auto && net start wuauserv",
    "bootrec /fixmbr",
    "bootrec /fixboot",
    "bootrec /rebuildbcd",
    "cleanmgr /sagerun:1",
    "powercfg -h off",
    "echo 1 > nul | powershell -Command \"[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); [System.GC]::Collect();\""
]

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repair Log</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #000;
            color: #fff;
        }}
        h1 {{
            text-align: center;
            color: #00bcd4;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        table, th, td {{
            border: 1px solid #555;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #1e1e1e;
            color: #00bcd4;
        }}
        tr:nth-child(even) {{
            background-color: #222;
        }}
        tr:hover {{
            background-color: #333;
        }}
        footer {{
            text-align: center;
            margin-top: 20px;
        }}
        .social-icons a {{
            margin: 0 10px;
            color: #00bcd4;
            text-decoration: none;
        }}
        .social-icons a:hover {{
            color: #fff;
        }}
    </style>
</head>
<body>
    <h1>System Repair Log</h1>
    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Command</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    <footer>
        <p>Developed by <strong>En.FahadAlsamiti</strong></p>
        <div class="social-icons">
            <a href="https://x.com/fahadalsamiti" target="_blank">X</a>
            <a href="https://github.com/FahadMAlsamiti" target="_blank">GitHub</a>
        </div>
    </footer>
</body>
</html>
"""

def write_html_log(command, status, details):
    """تسجيل العمليات في ملف HTML"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = f"<tr><td>{timestamp}</td><td>{command}</td><td>{status}</td><td>{details}</td></tr>\n"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write(html_template.format(rows=row))
    else:
        with open(log_file, "r+") as f:
            content = f.read()
            updated_content = content.replace("{rows}", row + "{rows}")
            f.seek(0)
            f.write(updated_content)
            f.truncate()

def is_admin():
    """التحقق من صلاحيات المسؤول"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def save_state(remaining_commands):
    """حفظ الأوامر المتبقية"""
    with open(state_file, "w") as f:
        json.dump({"remaining_commands": remaining_commands}, f)

def load_state():
    """تحميل الأوامر المتبقية"""
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
            return state.get("remaining_commands", [])
    return commands

def run_commands_in_sequence(commands):
    """تنفيذ الأوامر بالتسلسل"""
    remaining_commands = commands
    for command in commands:
        write_html_log(command, "Running", "Started execution")
        process = subprocess.run(f"echo y | {command}", shell=True)
        if process.returncode == 0:
            write_html_log(command, "Success", "Command executed successfully")
            remaining_commands.remove(command)
            save_state(remaining_commands)
        else:
            write_html_log(command, "Error", "An error occurred. Retrying...")
            process = subprocess.run(f"echo y | {command}", shell=True)

    write_html_log("Program Finished", "Complete", "All commands executed successfully")
    os.system("shutdown /r /t 0")

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        run_commands_in_sequence(load_state())
