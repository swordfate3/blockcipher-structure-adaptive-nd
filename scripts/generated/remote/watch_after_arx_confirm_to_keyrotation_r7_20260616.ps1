$ErrorActionPreference = "Stop"
$Root = "G:\lxy"
$ProjectId = "blockcipher-structure-adaptive-nd"
$ProjectPath = Join-Path $Root $ProjectId
$RunRoot = Join-Path $Root "$ProjectId-runs"
$LogDir = Join-Path $RunRoot "launcher_logs"
$UpstreamRun = "innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616"
$NextRun = "innovation1-arx-speck32-partial-inverse-keyrotation-r7-screen-gpu1-20260616"
$UpstreamBranch = "results/$UpstreamRun"
$NextScheduleScript = "G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\schedule_innovation1_arx_speck32_partial_inverse_keyrotation_r7_screen_gpu1_20260616.cmd"
$LogPath = Join-Path $LogDir "watch_after_innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616_to_innovation1-arx-speck32-partial-inverse-keyrotation-r7-screen-gpu1-20260616.log"
$PollSeconds = 600
$GpuIndex = 1
$Branch = "refactor/model-project-structure"
$env:GIT_SSH_COMMAND = "ssh -i C:/Users/1304Lijinlin/.ssh/github_blockcipher_20260612_result_pusher_ed25519 -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
function Write-WatchLog { param([string]$Message) $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"; "[$stamp] $Message" | Tee-Object -FilePath $LogPath -Append }
function Test-ResultBranch { param([string]$BranchName) Push-Location $ProjectPath; try { $line = & git ls-remote --heads origin $BranchName 2>&1; if ($LASTEXITCODE -eq 0 -and $line -match [regex]::Escape($BranchName)) { return $true }; if ($line) { Write-WatchLog "git output while checking $BranchName: $line" }; return $false } finally { Pop-Location } }
function Sync-Project { Push-Location $ProjectPath; try { & git fetch origin $Branch 2>&1 | Tee-Object -FilePath $LogPath -Append; & git checkout $Branch 2>&1 | Tee-Object -FilePath $LogPath -Append; & git merge --ff-only FETCH_HEAD 2>&1 | Tee-Object -FilePath $LogPath -Append; & git rev-parse --short HEAD 2>&1 | Tee-Object -FilePath $LogPath -Append; if ($LASTEXITCODE -ne 0) { throw "remote project sync failed" } } finally { Pop-Location } }
function Get-GpuUuid { $rows = & nvidia-smi --query-gpu=index,uuid --format=csv,noheader 2>&1; foreach ($row in $rows) { $parts = $row -split ","; if ($parts.Count -ge 2 -and $parts[0].Trim() -eq [string]$GpuIndex) { return $parts[1].Trim() } }; return $null }
function Get-TrainingProcessesOnGpu { param([string]$GpuUuid) $gpuRows = & nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name --format=csv,noheader 2>&1; $pids = @(); foreach ($row in $gpuRows) { $parts = $row -split ","; if ($parts.Count -ge 3 -and $parts[0].Trim() -eq $GpuUuid -and $parts[2] -match "python\.exe") { $pids += $parts[1].Trim() } }; $training = @(); foreach ($pidText in $pids) { try { $p = Get-CimInstance Win32_Process -Filter "ProcessId = $([int]$pidText)" } catch { continue }; if ($p -and $p.CommandLine -match "run_innovation_one_matrix\.py" -and $p.CommandLine -match "--device cuda:$GpuIndex") { $training += "$pidText $($p.CommandLine)" } }; return $training }
while ($true) {
  Write-WatchLog "Checking upstream branch $UpstreamBranch before launching $NextRun"
  if (Test-ResultBranch -BranchName "results/$NextRun") { Write-WatchLog "Result branch already exists for $NextRun; exiting"; exit 0 }
  if (-not (Test-ResultBranch -BranchName $UpstreamBranch)) { Write-WatchLog "Upstream branch not ready; sleeping ${PollSeconds}s"; Start-Sleep -Seconds $PollSeconds; continue }
  $gpuUuid = Get-GpuUuid
  if (-not $gpuUuid) { Write-WatchLog "Unable to resolve GPU$GpuIndex UUID; sleeping ${PollSeconds}s"; Start-Sleep -Seconds $PollSeconds; continue }
  $training = Get-TrainingProcessesOnGpu -GpuUuid $gpuUuid
  if ($training.Count -gt 0) { Write-WatchLog "GPU$GpuIndex busy with training process(es):"; foreach ($line in $training) { Write-WatchLog $line }; Start-Sleep -Seconds $PollSeconds; continue }
  Write-WatchLog "Upstream ready and GPU$GpuIndex free; syncing and launching $NextRun"
  Sync-Project
  Push-Location $ProjectPath
  try { & cmd.exe /c $NextScheduleScript 2>&1 | Tee-Object -FilePath $LogPath -Append; $exit = $LASTEXITCODE } finally { Pop-Location }
  Write-WatchLog "Next schedule script exited with code $exit"
  exit $exit
}
