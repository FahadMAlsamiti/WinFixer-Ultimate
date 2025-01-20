import subprocess
import os
import time
import ctypes
import sys
import json
from datetime import datetime

# اسم ملف تسجيل التقارير كصفحة HTML
log_file = "repair_log_with_chkdsk.html"
# اسم ملف الحالة لتخزين الأوامر المتبقية
state_file = "repair_state_with_chkdsk.json"

# تعريف الأوامر بالترتيب
commands = [
    "chkdsk /f /r",
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
    "cleanmgr /sagerun:1",
    "powercfg -h off",
    "echo 1 > nul | powershell -Command \"[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); [System.GC]::Collect();\""
]

# HTML القالب الأساسي لصفحة
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
            background-color: #f9f9f9;
            color: #333;
        }}
        h1 {{
            text-align: center;
            color: #0056b3;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        table, th, td {{
            border: 1px solid #ddd;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f1f1f1;
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
</body>
</html>
"""

def write_html_log(command, status, details):
    """تسجيل العملية في ملف HTML"""
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
    """التحقق مما إذا كان البرنامج يعمل بصلاحيات المسؤول"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def save_state(remaining_commands):
    """حفظ الأوامر المتبقية في ملف"""
    with open(state_file, "w") as f:
        json.dump({"remaining_commands": remaining_commands}, f)

def load_state():
    """تحميل الأوامر المتبقية من الملف"""
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
            return state.get("remaining_commands", [])
    return commands

def run_commands_in_sequence(commands):
    """تشغيل الأوامر بالترتيب والتعامل مع الأخطاء"""
    remaining_commands = commands
    for command in commands:
        write_html_log(command, "Running", "Started execution")
        process = subprocess.run(f"echo y | {command}", shell=True)
        if process.returncode == 0:
            write_html_log(command, "Success", "Command executed successfully")
            remaining_commands.remove(command)
            save_state(remaining_commands)
        elif "chkdsk" in command:
            write_html_log(command, "Restart Required", "chkdsk needs a restart to complete.")
            save_state(remaining_commands)
            os.system("shutdown /r /t 0")
            return
        else:
            write_html_log(command, "Error", "An error occurred during execution")

def register_autorun():
    """إضافة البرنامج إلى التشغيل التلقائي"""
    # إعداد التشغيل التلقائي...
    pass

def unregister_autorun():
    """إزالة البرنامج من التشغيل التلقائي"""
    # إزالة التشغيل التلقائي...
    pass

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        commands_to_execute = load_state()
        run_commands_in_sequence(commands_to_execute)