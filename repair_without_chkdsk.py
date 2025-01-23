import subprocess
import os
import time
import ctypes
import sys
import json
import platform
from datetime import datetime

# إعداد التقارير
log_file = "repair_log_without_chkdsk.html"
state_file = "repair_state_without_chkdsk.json"

# تعريف الأوامر بالترتيب
commands = [
    # Windows Update Repair
    "net stop wuauserv",
    "net stop bits",
    "net stop cryptSvc",
    "net stop msiserver",
    "ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old",
    "ren C:\\Windows\\System32\\catroot2 catroot2.old",
    "net start wuauserv",
    "net start bits",
    "net start cryptSvc",
    "net start msiserver",

    # System Repair
    "DISM /Online /Cleanup-Image /CheckHealth",
    "DISM /Online /Cleanup-Image /ScanHealth",
    "DISM /Online /Cleanup-Image /RestoreHealth",
    "DISM /Online /Cleanup-Image /StartComponentCleanup",
    "DISM /Online /Cleanup-Image /AnalyzeComponentStore",
    "DISM /Online /Cleanup-Image /RestoreHealth /Source:C:\\RepairSource\\Windows",
    "SFC /scannow",

    # Disk Cleanup
    "del /s /q %temp%\\*",
    "del /s /q C:\\Windows\\Temp\\*",
    "del /s /q C:\\Windows\\Prefetch\\*",

    # Network Repair
    "ipconfig /release",
    "ipconfig /renew",
    "ipconfig /flushdns",
    "netsh int ip reset",
    "netsh winsock reset",
    "netsh advfirewall reset",
    "ping 8.8.8.8 -n 4",
    'netsh interface ipv4 set dns name="Ethernet" source=static address=8.8.8.8',
    'netsh interface ipv4 add dns name="Ethernet" address=8.8.4.4 index=2',
    'netsh interface ipv6 set dns name="Ethernet" source=static address=2001:4860:4860::8888',
    'netsh interface ipv6 add dns name="Ethernet" address=2001:4860:4860::8844 index=2',

    # Driver Repair
    "pnputil /scan-devices",
    "pnputil /reinstall-device *",
    "driverquery /fo csv > drivers.csv",
    "devcon restart *display*",
    "devcon restart *net*",

    # General Maintenance
    "eventvwr",
    "mrt /F",
    "cleanmgr /sagerun:1",
    "powercfg /hibernate off",
    "winget upgrade --all",
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
    <h2>System Information</h2>
    <table>
        <tr><th>Host Name</th><td>{host_name}</td></tr>
        <tr><th>OS Name</th><td>{os_name}</td></tr>
        <tr><th>OS Version</th><td>{os_version}</td></tr>
        <tr><th>Original Install Date</th><td>{install_date}</td></tr>
        <tr><th>System Manufacturer</th><td>{system_manufacturer}</td></tr>
        <tr><th>System Model</th><td>{system_model}</td></tr>
    </table>
    <h2>Repair Operations</h2>
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

def collect_system_info():
    """جمع معلومات النظام"""
    system_info = subprocess.getoutput("systeminfo")
    return {
        "host_name": platform.node(),
        "os_name": subprocess.getoutput("systeminfo | findstr /B /C:'OS Name'").split(":")[1].strip(),
        "os_version": subprocess.getoutput("systeminfo | findstr /B /C:'OS Version'").split(":")[1].strip(),
        "install_date": get_install_date(system_info),
        "system_manufacturer": subprocess.getoutput("wmic computersystem get manufacturer").split("\n")[1].strip(),
        "system_model": subprocess.getoutput("wmic computersystem get model").split("\n")[1].strip()
    }

def get_install_date(system_info):
    """استخراج تاريخ التثبيت من systeminfo"""
    for line in system_info.splitlines():
        if "Original Install Date" in line:
            return line.split(":")[1].strip()
    return "N/A"

def write_html_log(command, status, details, system_info=None):
    """تسجيل العمليات في ملف HTML"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = f"<tr><td>{timestamp}</td><td>{command}</td><td>{status}</td><td>{details}</td></tr>\n"

    if not os.path.exists(log_file):
        # Create the HTML file with the initial template and system info
        with open(log_file, "w") as f:
            f.write(html_template.format(rows=row, **system_info))
    else:
        # Append the new row to the existing HTML file
        with open(log_file, "r+") as f:
            content = f.read()
            # Find the position of </tbody> and insert the new row before it
            tbody_end = content.find("</tbody>")
            if tbody_end != -1:
                updated_content = content[:tbody_end] + row + content[tbody_end:]
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
    system_info = collect_system_info()
    remaining_commands = commands
    for command in commands:
        write_html_log(command, "Running", "Started execution", system_info)
        try:
            process = subprocess.run(f"echo y | {command}", shell=True, timeout=300, capture_output=True, text=True)
            if process.returncode == 0:
                write_html_log(command, "Success", "Command executed successfully", system_info)
                remaining_commands.remove(command)
                save_state(remaining_commands)
            else:
                write_html_log(command, "Error", f"An error occurred: {process.stderr}", system_info)
        except subprocess.TimeoutExpired:
            write_html_log(command, "Timeout", "Command timed out after 5 minutes", system_info)
        except Exception as e:
            write_html_log(command, "Error", f"An unexpected error occurred: {str(e)}", system_info)

    # حذف ملف الحالة بعد النجاح
    if os.path.exists(state_file):
        os.remove(state_file)

    # استفسار لإعادة التشغيل
    user_choice = input("\nAll commands executed successfully! Do you want to restart the system now? (y/n): ")
    if user_choice.lower() == "y":
        os.system("shutdown /r /t 0")
    else:
        print("System restart skipped.")

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        run_commands_in_sequence(load_state())