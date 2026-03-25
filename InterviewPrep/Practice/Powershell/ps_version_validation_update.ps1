$path = 'HKLM:\SOFTWARE\GeForceNow\Build\CurrentVersion'
$CurrentBuildNo = 'Version'
$exp_build = [version] "4.2.1"
$log = "C:\Logs\build_validation.log"
$logDir = Split-Path $log
# $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss" || this timestamp will capture once and return the same entry for each log input.
# instead use put it in a function that needs to be rerun each time
function Get-Timestamp {
    Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

#guarded log entry to ensure the log file exists before writing 
if (-not(Test-Path $log)){
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

#verify registry key exists
if (-not(Test-Path -Path $path)){
    Add-Content $log "$(Get-Timestamp) Registry key not found: $path"
    exit
}

#read the installed build number from the registry
$installedVersion = [version] (Get-ItemProperty -Path $path -Name $CurrentBuildNo -ErrorAction SilentlyContinue | Select-Object -ExpandProperty $CurrentBuildNo)

# compares the current build number with the expected build number
if ($null -eq $installedVersion){
    Add-Content $log "$(Get-Timestamp) Build number not found."
}
elseif ($installedVersion -ge $exp_build){
    Add-Content $log "$(Get-Timestamp) Build number is valid: $installedVersion"
}
else {
    Add-Content $log "$(Get-Timestamp) Build number is invalid: $installedVersion. Expected: $exp_build or higher."
    Start-Process -FilePath "C:\GeForceNow\updater\update.exe" -WindowStyle Hidden -ArgumentList "/silent"
}
