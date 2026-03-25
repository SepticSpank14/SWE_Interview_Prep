# GeForce NOW receives a JSON feed from a publisher containing game session telemetry. Your job is to parse the feed, flag any sessions with performance issues, and write a report.
# Write a Python script that:

# 1 Reads a JSON file at C:\Data\session_telemetry.json
# 2 Each record has these fields: session_id, game_title, fps, latency_ms, gpu_utilization, and region
# 3 Flags a session as having a performance issue if ANY of the following are true:

#       fps is below 30
#       latency_ms is above 100
#       gpu_utilization is below 20 or above 95


# 4 Writes flagged sessions to C:\Data\flagged_sessions.csv with all original fields plus a new column flag_reason containing a comma-separated list of reasons
# 5 Logs each flagged session with timestamp and reasons to C:\Logs\telemetry_review.log
# 6 Prints and logs a summary — total sessions, flagged count, clean count

import pandas as pd
import json
import os
from datetime import datetime

jData_file = r"C:\Data\session_telemetry.json"
flagged_file = r"C:\Data\flagged_sessions.csv"
log_path = r"C:\Logs\telemetry_review.log"
required_fields = ['session_id', 'game_title', 'fps', 'latency_ms', 'gpu_utilization', 'region']

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# check if log exists, if not make it, then format the log input structure
os.makedirs(os.path.dirname(log_path), exist_ok=True)
def log(message, log_path):
    with open (log_path, "a") as f:
        f.write(f"[{timestamp()}] - {message}\n")

#Read the json file and convert to object 
with open(jData_file, 'r') as f:
    jData_file = json.load(f)

flagged_records = []
session_Count = 0
flagged_count = 0
clean_count = 0

for record_item in jData_file: # loop over the records within the file
    flag_reason = []
    is_Flagged = False
    session_Count += 1

    # check for all required fields
    for field in required_fields:
        if field not in record_item or not record_item[field]:
            is_Flagged = True
            flag_reason.append(f"missing or empty field: {field}")

    # check if fps is below 30    
    if record_item.get('fps') is not None and record_item.get('fps') < 30:
        is_Flagged = True
        flag_reason.append(f"fps is below 30")

    # check if latency is above 100ms
    if record_item.get('latency_ms') is not None and record_item.get('latency_ms')> 100:
        is_Flagged = True
        flag_reason.append(f"High latency: >100ms")
    
    #get the 'gpu_utilization' key, assign it to gpu, and check that it is within 20 - 95
    gpu = record_item.get('gpu_utilization')
    if gpu is not None and (gpu < 20 or gpu > 95):
    # if record_item.get('gpu_utilization') < 20 or ('gpu_utilization') > 95:
        is_Flagged = True
        flag_reason.append(f"GPU utilization outside of optimal range")

    if is_Flagged:
        #english "record_item" is a dictionary, define "flag_reason" key with values joined by ", "
        record_item['flag_reason'] = ", ".join(flag_reason)
        flagged_records.append(record_item)
        #use a pd.DataFrame at the end to write the record, don't manually insert it
        # with open(flagged_file, "a") as f:
        #     f.write(f"[{flagged_records}] \n")
        log(f"{timestamp()} - {record_item}", log_path)
        flagged_count += 1
    else: 
        clean_count += 1

#write results to csv and log the summary
pd.DataFrame(flagged_records).to_csv(flagged_file, index=False)
log(f"{timestamp()} SUMMARY: total - {session_Count} | flagged - {flagged_count} | clean - {clean_count}", log_path)