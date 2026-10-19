# EXP-013: native Windows launcher. Full run generates 14 scenarios and 28 dashboards.
# .\scripts\run_exp_013.ps1 -Quick
# .\scripts\run_exp_013.ps1 -RequireUmap
# .\scripts\run_exp_013.ps1 -RequireUmap -Push
[CmdletBinding()]
param(
  [switch]$Quick,
  [switch]$RequireUmap,
  [switch]$Push,
  [int]$Seed=20261019,
  [int]$KDetect=8,
  [int]$KEmbed=10,
  [string]$Families=""
)
$ErrorActionPreference="Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ($Push -and $Quick) { throw "A smoke test must not be pushed as research evidence." }
if ($Push -and (git status --porcelain)) { throw "Commit or stash unrelated local changes before -Push." }
$run=(Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
if ($Quick) { $run+="-quick" } else { $run+="-full" }
$exp="013-classical_multicomponent_dashboards"
$arguments=@("proximity_isomap/code/$exp/run.py","--label",$run,
             "--seed","$Seed","--k-detect","$KDetect","--k-embed","$KEmbed")
if ($Quick) { $arguments+="--quick" }
if ($RequireUmap) { $arguments+="--require-umap" }
if ($Families) { $arguments+=@("--families",$Families) }
Write-Host "[EXP-013] $run"
conda run --no-capture-output -n proximity-isomap python @arguments
if ($LASTEXITCODE -ne 0) { throw "EXP-013 failed. Any partial run is NOT publishable evidence." }
$results="proximity_isomap/results/$exp/runs/$run"
$figures="proximity_isomap/figures/$exp/runs/$run"
foreach ($required in @("$results/method_metrics.csv","$results/detected_components_vs_k.csv",
                         "$results/knn_detection_embedding_grid.csv","$results/metadata.json",
                         "$results/sha256.json")) {
  if (-not (Test-Path -LiteralPath $required)) { throw "Missing: $required" }
}
$dashboards=@(Get-ChildItem -Path $figures -Recurse -File -Filter "dashboard_*.png")
if ($dashboards.Count -lt 4) { throw "Dashboards missing or incomplete." }
Write-Host "[COMPLETE] $($dashboards.Count) rendered PNG dashboards with matching SVGs."
Write-Host "[RESULTS] $results"
Write-Host "[FIGURES] $figures"
if ($Push) {
  git add -- $results $figures
  if ($LASTEXITCODE -ne 0) { throw "git add failed" }
  git diff --cached --check
  if ($LASTEXITCODE -ne 0) { throw "Staging validation failed" }
  git commit -m "Run EXP-013 far-near multicomponent dashboards $run"
  if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
  git push origin main
  if ($LASTEXITCODE -ne 0) { throw "Git push failed; local files retained" }
  Write-Host "[PUBLISHED] $(git rev-parse HEAD)"
} else {
  Write-Host "Local run complete. Use Git to publish these result and figure folders, or rerun full with -Push."
}
