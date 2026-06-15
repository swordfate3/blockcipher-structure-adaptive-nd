$ErrorActionPreference = "Stop"

$Root = "G:\lxy"
$ProjectId = "blockcipher-structure-adaptive-nd"
$ProjectPath = Join-Path $Root $ProjectId
$RunRoot = Join-Path $Root "$ProjectId-runs"
$LogDir = Join-Path $RunRoot "launcher_logs"
$UpstreamRun = "innovation1-spn-present-delta-sinv-beam4deep3-r7-gpu1-20260616"
$NextRun = "innovation1-spn-present-delta-sinv-beamstats4deep3-r7-gpu1-20260616"
$UpstreamBranch = "results/$UpstreamRun"
$NextScheduleScript = Join-Path $ProjectPath "scripts\generated\remote\schedule_innovation1_spn_present_delta_sinv_beamstats4deep3_r7_gpu1_20260616.cmd"
$LogPath = Join-Path $LogDir "watch_after_${UpstreamRun}_to_${NextRun}.log"
$PollSeconds = 600
$env:GIT_SSH_COMMAND = "ssh -i C:/Users/1304Lijinlin/.ssh/github_blockcipher_20260612_result_pusher_ed25519 -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-WatchLog {
    param([string]$Message)
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$stamp] $Message" | Tee-Object -FilePath $LogPath -Append
}

while ($true) {
    Write-WatchLog "Checking upstream branch $UpstreamBranch before launching $NextRun"
    Push-Location $ProjectPath
    try {
        $branchLine = & git ls-remote --heads origin $UpstreamBranch 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($exitCode -eq 0 -and $branchLine -match $UpstreamBranch) {
        Write-WatchLog "Upstream branch found; launching $NextScheduleScript from $ProjectPath"
        Push-Location $ProjectPath
        try {
            & cmd.exe /c $NextScheduleScript 2>&1 | Tee-Object -FilePath $LogPath -Append
            $scheduleExit = $LASTEXITCODE
        }
        finally {
            Pop-Location
        }
        Write-WatchLog "Next schedule script exited with code $scheduleExit"
        exit $scheduleExit
    }

    Write-WatchLog "Upstream not ready yet; git exit=$exitCode; sleeping ${PollSeconds}s"
    if ($branchLine) {
        Write-WatchLog "git output: $branchLine"
    }
    Start-Sleep -Seconds $PollSeconds
}
