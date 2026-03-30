# You're back on the GeForce NOW platform team. A new monitoring requirement has come in — the team needs a Python script that can be scheduled to run every 15 minutes on a streaming node to verify critical processes are running, log any anomalies, and write a simple status file that an upstream health dashboard can poll.
import psutil
import sys
import json
import os
from datetime import datetime

EXPECTED_PROCS = ["nvcontainer.exe", "nvtelemetry.exe", "GfeSDKService.exe", "nvdisplay.container.exe"]
OUTPUT_FILE = r"C:\Status\node_status.json"
log_file = r"C:\Logs\watchdog\watchdog.log"

#settup timestamp
def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#settup logging
def log (message, path=log_file):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp()}] - {message}\n")

#check running expected processes
def check_proc():
    missing = []
    healthy = []

    try:
        running = {p.info['name'].lower() for p in psutil.process_iter(['name'])} # EXPECT_PROCS is a list of expected process names. We use psutil to iterate over ALL RUNNING PROCESSES and collect their names in a set called running. This allows us to easily check which expected processes are currently running on the system.

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            log(f"Error enumerating processes: {e}")
            sys.exit(1) # exception block only handles exception, the actual process check is done inside the normal flow 

    for proc in EXPECTED_PROCS:
        if proc.lower() in running:
            log(f"{proc} - RUNNING", log_file)
            healthy.append(proc)
        else:
            log(f"{proc} - MISSING", log_file)
            missing.append(proc)
            status = "DEGRADED"

    status = "DEGRADED" if missing else "OK"

    if not missing:
        log(f"STATUS: {status} - ALL PROCESSES RUNNING", log_file)

    else:
        log(f"STATUS: {status} - MISSING: {', '.join(missing)}", log_file)

    #define payload to write to json
    payload = {
        "timestamp": timestamp(),
        "status": "DEGRADED" if missing else "OK", #simple if then
        "missing": missing,
        "healthy": healthy,
    }

    #write payload to json
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True) #just like with the log, you need to guard the json file too
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(payload, f, indent=2)

    sys.exit (1 if missing else 0)

if __name__ == "__main__":
    check_proc()