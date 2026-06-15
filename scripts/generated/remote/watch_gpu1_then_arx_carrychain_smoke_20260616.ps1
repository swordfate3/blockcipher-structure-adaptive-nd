$ErrorActionPreference = "Stop"

$Root = "G:\lxy"
$ProjectId = "blockcipher-structure-adaptive-nd"
$ProjectPath = Join-Path $Root $ProjectId
$RunRoot = Join-Path $Root "$ProjectId-runs"
$LogDir = Join-Path $RunRoot "launcher_logs"
$RunId = "innovation1-arx-speck32-carrychain-smoke-gpu1-20260616"
$GpuIndex = "1"
$ScheduleScript = Join-Path $ProjectPath "scripts\generated\remote\schedule_innovation1_arx_speck32_carrychain_smoke_gpu1_20260616.cmd"
$LogPath = Join-Path $LogDir "watch_${RunId}_gpu${GpuIndex}.log"
$PollSeconds = 300

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-WatchLog {
    param([string]$Message)
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$stamp] $Message" | Tee-Object -FilePath $LogPath -Append
}

function Get-GpuUuid {
    $rows = & nvidia-smi --query-gpu=index,uuid --format=csv,noheader
    foreach ($row in $rows) {
        $parts = $row -split ","
        if ($parts.Count -ge 2 -and $parts[0].Trim() -eq $GpuIndex) {
            return $parts[1].Trim()
        }
    }
    return $null
}

function Test-GpuPythonBusy {
    param([string]$GpuUuid)
    $rows = & nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name --format=csv,noheader 2>$null
    foreach ($row in $rows) {
        $parts = $row -split ","
        if ($parts.Count -ge 3 -and $parts[0].Trim() -eq $GpuUuid -and $parts[2].Trim() -match "python\.exe$") {
            Write-WatchLog "GPU${GpuIndex} busy: $row"
            return $true
        }
    }
    return $false
}

while ($true) {
    Write-WatchLog "Checking GPU${GpuIndex} before launching $RunId"
    $gpuUuid = Get-GpuUuid
    if (-not $gpuUuid) {
        Write-WatchLog "Could not resolve GPU${GpuIndex}; sleeping ${PollSeconds}s"
        Start-Sleep -Seconds $PollSeconds
        continue
    }

    if (Test-GpuPythonBusy -GpuUuid $gpuUuid) {
        Write-WatchLog "GPU${GpuIndex} still busy; sleeping ${PollSeconds}s"
        Start-Sleep -Seconds $PollSeconds
        continue
    }

    Write-WatchLog "GPU${GpuIndex} appears idle; launching $ScheduleScript from $ProjectPath"
    Push-Location $ProjectPath
    try {
        & cmd.exe /c $ScheduleScript 2>&1 | Tee-Object -FilePath $LogPath -Append
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    Write-WatchLog "Schedule script exited with code $exitCode"
    exit $exitCode
}
