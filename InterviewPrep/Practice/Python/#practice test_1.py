#practice test
import os
import csv
from datetime import datetime
from packaging import version

input_file = r'C:\Data\driver_inventory.csv'
driver_version = '527.56'
log_file = r'C:\Logs\driver_audit\audit.log'

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def log(message, path=log_file):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a') as f:
        f.write(f"[{timestamp()}] - {message}\n")

result = []
failed = []

#check if file exists
if os.path.isfile(input_file):
    log(f"Input file found", log_file)
else:
    log(f"Input file not found", log_file)
    exit(1)


with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        "hostname": row['hostname'],
        "driver_str": row.get('driver_version'), # .get for safety
        "region": row['region']
        
        if parse(row['driver_version']) >= parse(driver_version):
            status = 'PASS'
            log(f"{hostname} ({region }): {driver_str} - PASS", log_file)
        else:
            status = 'FAIL'
            log(f"{hostname} ({region }): {driver_str} - FAIL", log_file)
            failed.append(hostname)
        
        results.append({'hostname': hostname, 'driver_version': driver_str, 'region': region, 'status': status})

total_tests = len(results)
passed_test = len(results) - len(failed)

log(f"SUMMARY - {passed_test} / {total_tests} nodes compliant. FAILED: {failed}", log_file)