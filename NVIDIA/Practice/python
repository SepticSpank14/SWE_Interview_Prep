# THINGS TO KEEP IN MIND:
# Timestamps on every log entry — every single write
# Guard the log directory — os.makedirs before you touch the log file
# Independent checks — never nest; collect all results, evaluate at the end

import os
import json
from datetime import datetime #explicitly asked for datetime stamps. Use this library

key = "version"
value = "2.1"
game_launch_path = "C:/Games/LaunchGame/LaunchGame.exe"
License_file_path = "C:/Games/LaunchGame/License/License.dat"
settings_file_path = "C:/Games/LaunchGame/config/settings.json" 
log_file_path = "C:/Logs/onboarding_validation.log"

# definte the timestamp function to return the current date and time in a readable format. This will be used for logging purposes to track when each check was performed.
def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# define a logging function that takes a message and a log file path as arguments. This function will append the message to the specified log file, prefixed with a timestamp for better tracking of events.
def log(message, log_file_path):
    with open(log_file_path, "a") as f: # 'A' stands for 'append' mode, which allows you to add new content to the end of the file without overwriting existing content. 
        # If the file does not exist, it will be created. 
        f.write(f"[{timestamp()}] {message}\n")

# definte a function to check for key value pairs in settings.json file. TRY to read the settings file path and
def check_key_value_in_json(settings_file_path, key, value):
    try:
        with open(settings_file_path, "r") as f: 
            # "with open" is the preferred way to handle file operations in Python as it ensures that the file is properly closed after its suite finishes, even if an exception is raised. 
            #This prevents potential memory leaks and ensures that resources are managed efficiently.
            # "f" (or file_object) is a variable that represents the opened file. It allows you to read from or write to the file using methods like 
            # read(), readline(), or write().
            data = json.load(f)
        return data.get(key) == value
    except Exception as e:
        return False
    
    # with open(settings_file_path, "r") as f:
    #     data = json.load(f)
    # if data.get(key) == value:
    #     return True
    # else:
    #     return False

# Run all checks independently
results = []

# Check 1 — Executable
if os.path.isfile(game_launch_path):
    log("PASS: Game executable found", log_file_path)
    results.append(True)
else:
    log("FAIL: Game executable not found", log_file_path)
    results.append(False)

# Check 2 — License file
if os.path.isfile(license_file_path):
    log("PASS: License file found", log_file_path)
    results.append(True)
else:
    log("FAIL: License file not found", log_file_path)
    results.append(False)

# Check 3 — Config key-value
if os.path.isfile(settings_file_path):
    if check_key_value_in_json(settings_file_path, key, value):
        log(f"PASS: Config key '{key}' matches value '{value}'", log_file_path)
        results.append(True)
    else:
        log(f"FAIL: Config key '{key}' does not match expected value '{value}'", log_file_path)
        results.append(False)
else:
    log("FAIL: Config file not found", log_file_path)
    results.append(False)

# Final summary
if all(results):
    log("SUMMARY: All checks passed. Game ready for onboarding.", log_file_path)
    print("PASS: All validation checks passed.")
else:
    log("SUMMARY: One or more checks failed. Review log for details.", log_file_path)
    print("FAIL: Validation failed. Review log for details.")

# WHY THIS IS WRONG: The original code was structured in a way that if any of the checks failed (game executable, license file, or settings file), 
# it would not proceed to check the remaining conditions. This means that if the game executable was missing, it would not check for the license file or the settings file, 
# which could lead to incomplete validation and less informative logging. Each check should be performed independently to ensure that all potential issues are 
# identified and logged, providing a comprehensive overview of the validation process.
# 
# try:
#     if os.path.exists(game_launch_path):
#         if os.path.isfile(License_file_path):
#             if os.path.exists(settings_file_path):
#                 check_key_value_in_json(settings_file_path, key, value)
#                 with open(log_file_path, "a") as f:
#                     f.write(f"Checked {key} in settings.json and found value: {value}\n")
#                 print("Game and license found. Ready to launch!")
#             else:
#                 with open(log_file_path, "a") as f:
#                     f.write("Settings file not found. Please ensure settings.json is in the correct directory.\n")
#         else:
#             with open(log_file_path, "a") as f:
#                 f.write("License file not found. Please ensure License.dat is in the correct directory.\n")
#     else:
#         with open(log_file_path, "a") as f:
#             f.write("Game executable not found. Please ensure LaunchGame.exe is in the correct directory.\n")
# except Exception as e:
#     with open(log_file_path, "a") as f:
#         f.write(f"An error occurred: {e}\n")