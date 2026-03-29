# You're supporting a GeForce NOW streaming node fleet. Before a node is cleared for active game sessions, it needs to pass a pre-flight check. 
# A ticket has come in — some nodes are being cleared despite having stale driver versions or stopped display services.
# Your job: Write a PowerShell script that performs a pre-flight check on the local node by doing two things:

# Registry check — Read the installed NVIDIA driver version from the registry and verify it meets the minimum required version
# Service check — Verify that NVDisplay.ContainerLocalSystem is running

$reg_path = 'HKLM:\SOFTWARE\NVIDIA Corporation\Global\GMSystem'
$reg_val = 'DriverVersion'
$min_ver = [version]'527.56'
$svc_to_check = 'NVDisplay.ContainerLocalSystem'
$log_path = 'c:\Logs\preflight\preflight.log'
$LOG_DIR = Split-Path $log_path
$failed = 0

#timestamp for log
function Get-Timestamp {
    return Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
}
#guarded logs, double check that it's against the DIRECTORY not the path
if (-not(Test-Path $LOG_DIR)){
    New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null
}
# if (-not(Test-Path $log_path)){
#     New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null
# }

#verify the registry key exists and is readable. Also the timestamp goes in the logging for each check, python it only goes in the function
if(-not(Test-Path $reg_path)){
    Add-Content $log_path "$(Get-Timestamp)Registry key not found -- FAIL"
    $failed ++
}else{
    #read the installed build number from registry. Either terminate early or finish with else
    $current_build = [version](Get-ItemProperty -Path $reg_path).$reg_val
    # $current_build = [version] (Get-ItemProperty -Path $reg_path -Name $reg_val -ErrorAction SilentlyContinue) | Select-Object -ExpandProperty $reg_val
}

#compares build to $exp_build
if($null -eq $current_build){
    Add-Content $log_path "$(Get-Timestamp)$reg_val registry key not found - FAIL."
    $failed ++
} elseif ($current_build -lt $min_ver) {
    Add-Content $log_path "$(Get-Timestamp)${reg_val}: $current_build - FAIL"
    $failed ++   
} else {
    Add-Content $log_path "$(Get-Timestamp)${reg_val}: $current_build - PASS"
}

#check if service is running
try{
    $svc = Get-Service -Name $svc_to_check -ErrorAction Stop
} catch {
    Add-Content $log_path "$(Get-Timestamp) $svc_to_check service not found - FAIL."
    $failed ++
}

if($null -eq $svc){
    Add-Content $log_path "$(Get-Timestamp)$svc_to_check service not found - FAIL."
    $failed ++
} elseif ($svc.Status -ne 'Running') {
    Add-Content $log_path "$(Get-Timestamp)$svc_to_check - STOPPED"
    $failed ++
} else{
    Add-Content $log_path "$(Get-Timestamp)$svc_to_check - RUNNING"
}

#Log pre-flight pass or failed
if ($failed -eq 0){
    Add-Content $log_path "$(Get-Timestamp)PRE-FLIGHT: PASS"
    exit 0
} else {
    Add-Content $log_path "$(Get-Timestamp)PRE-FLIGHT: FAIL"
    exit 1
}
