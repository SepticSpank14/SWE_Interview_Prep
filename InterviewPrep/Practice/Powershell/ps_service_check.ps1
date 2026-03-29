# You're supporting a GeForce NOW streaming node. A ticket came in — 
# operators suspect that several critical NVIDIA services are either 
# stopped or stuck in a bad state after a recent patch deployment.
# Your job: Write a PowerShell script that checks the status of a list of critical services, 
#attempts to restart any that are stopped, logs all activity, and reports a final summary.

# Requirements:

# Service list (hardcoded):

#    "NvContainerLocalSystem", "NvContainerNetworkService", "NVDisplay.ContainerLocalSystem", "GfeSDKService"

# Log output to: C:\Logs\service_audit\audit.log
# Each log entry must include a timestamp
# For each service:

# If Running → log it, move on
# If Stopped → attempt to restart it, wait for it to reach Running state, then log success or failure
# If the service doesn't exist → log it and move on


# After all services checked, log a summary:

#    [2025-01-15 09:32:11] SUMMARY: 3/4 services healthy. RESTARTED: NvContainerLocalSystem. FAILED: GfeSDKService

# If all healthy:

#    [2025-01-15 09:32:11] SUMMARY: All services nominal.

# Exit code: 0 if all healthy, 1 if any failures

$SERVICES_TO_CHECK = @("NvContainerLocalSystem", "NvContainerNetworkService", "NVDisplay.ContainerLocalSystem", "GfeSDKService")
$LOG_FILE = 'C:\Logs\service_audit\audit.log'
$LOG_DIR = Split-Path $LOG_FILE

function Get-Timestamp {
    return Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

function Write-Log {
    param([string]$Message)
    if (-not (Test-Path $LOG_DIR)) {
        New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null
    }
    Add-Content $LOG_FILE "[$(Get-Timestamp)] $Message"
}

$restarted = @()
$failed = @()
$healthy = 0

foreach ($name in $SERVICES_TO_CHECK) {
    try {
        $svc = Get-Service -Name $name -ErrorAction Stop
    } catch {
        Write-Log "Service $name not found. Skipping."
        $failed += $name
        continue
    }

    if ($svc.Status -eq 'Running') {
        Write-Log "$name is Running."
        $healthy++
    } elseif ($svc.Status -eq 'Stopped') {
        Write-Log "$name is Stopped. Attempting restart..."
        try {
            Start-Service -Name $name -ErrorAction Stop
            $svc.WaitForStatus('Running', (New-TimeSpan -Seconds 30))
            $svc = Get-Service -Name $name
            if ($svc.Status -eq 'Running') {
                Write-Log "$name restarted successfully."
                $restarted += $name
                $healthy++
            } else {
                Write-Log "$name failed to reach Running state."
                $failed += $name
            }
        } catch {
            Write-Log "Error restarting $name - $_"
            $failed += $name
        }
    }
}

$total = $SERVICES_TO_CHECK.Count

if ($failed.Count -eq 0) {
    Write-Log "SUMMARY: All services nominal."
    exit 0
} else {
    Write-Log "SUMMARY: $healthy/$total services healthy. RESTARTED: $($restarted -join ', '). FAILED: $($failed -join ', ')"
    exit 1
}