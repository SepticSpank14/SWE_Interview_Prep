import os
import winreg
import psutil
from datetime import datetime

reg_path = r"Software\GeForceNOW\Games\LaunchGame"
LOG_FILE = r"C:\Logs\onboarding.log"
set_InstallPath = r"C:\Games\LaunchGame"
results = []

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# make log if it doesn't exits, and make sure the directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Check registry HKCU registry key for Launcher; log results to C:\Logs|onboarding.log, don't forget timestamp
def check_registry(reg_path):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        winreg.CloseKey(registry_key)
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp()} - Registry key found: {reg_path}\n")
        results.append(True)
        return True
    except FileNotFoundError:
        registry_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.CloseKey(registry_key)
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp()} - Registry key not found: {reg_path}. Registry key generated.\n")
        results.append(False)
        return False
    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp()} - Error checking registry key: {str(e)}\n")
        results.append(False)
        return False

def get_service_status(GameLicenseService):
    status = None
    service = None
    try: 
        service = psutil.win_service_get(GameLicenseService)
        if service: 
            service_dict = service.as_dict()
            status = service_dict.get('status')
            with open(LOG_FILE, "a") as log:
                log.write(f"{timestamp()} - Service '{GameLicenseService}' status: {status}\n")
    except psutil.NoSuchProcess as ex:
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp()} - Service '{GameLicenseService}' not found: {str(ex)}\n")
        results.append(False)
    
    # checks if the GameLicenseService is running; if not, attempt to start it and log the results to C:\Logs\onboarding.log, don't forget timestamp
    if status == 'running':
        with open(LOG_FILE, "a") as log:
            log.write(f"{timestamp()} - Game License Service is running.\n")
        results.append(True)
    elif status is not None:
        try:
            service.start()
            with open(LOG_FILE, "a") as log:
                log.write(f"{timestamp()} - Game License Service was not running and has been started.\n")
            results.append(True)
        except Exception as e:
            with open(LOG_FILE, "a") as log:
                log.write(f"{timestamp()} - Error starting Game License Service: {str(e)}\n")
            results.append(False)
    

# Set InstallPath key:value in registry if not set; log results to C:\Logs|onboarding.log, don't forget timestamp
if check_registry(reg_path):
    try: 
        update_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(update_key, "InstallPath", 0, winreg.REG_SZ, r"C:\Games\LaunchGame")
        winreg.CloseKey(update_key)
        with open(LOG_FILE, "a") as log:
            log.write(f"[{timestamp()}] - InstallPath registry key updated to: {set_InstallPath}\n")
            results.append(True)
    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"[{timestamp()}] - Error updating InstallPath registry key: {str(e)}\n")
            results.append(False)

get_service_status("GameLicenseService")
#create a summary of all previous actions and log it to C:\Logs|onboarding.log, don't forget timestamp
if all(results):
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp()}] - SUMMARY: All checks passed. Game ready for onboarding.\n")
    print("PASS: All validation checks passed.")
else:
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp()}] - SUMMARY: One or more checks failed. Review log for details.\n")
    print("FAIL: Validation failed. Review log for details.")