# Windows PowerShell: Conda setup, tests, EXP-001..008 rerun, SVG/PNG and Git.
# Call: .\scripts\run_all.ps1                  # full local run, no commit
#       .\scripts\run_all.ps1 -Quick            # quick smoke, no commit
#       .\scripts\run_all.ps1 -Push             # full run and git push
[CmdletBinding()]
param(
    [switch]$Quick,
    [switch]$Push,
    [int]$Seed = 20261018
)
$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSNativeCommandUseErrorActionPreference = $true
}
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    throw "Conda was not found. Install Miniforge or Miniconda and initialize PowerShell."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git was not found."
}
if ((git branch --show-current).Trim() -ne "main") {
    throw "Run from main (or review the script and choose the desired branch)."
}
$dirty = git status --porcelain
if ($dirty) { throw "Working tree is not clean. Commit/stash changes before running." }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull failed." }

$envName = "proximity-isomap"
$environments = conda env list --json | ConvertFrom-Json
$exists = @($environments.envs | Where-Object { (Split-Path $_ -Leaf) -eq $envName }).Count -gt 0
if ($exists) {
    Write-Host "[CONDA] Update $envName from environment.yml"
    conda env update -n $envName -f environment.yml --prune
} else {
    Write-Host "[CONDA] Create $envName from environment.yml"
    conda env create -f environment.yml
}
if ($LASTEXITCODE -ne 0) { throw "Conda environment setup failed." }

function Invoke-ResearchPython {
    param([string[]]$ArgsList)
    conda run --no-capture-output -n $envName python @ArgsList
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed: $($ArgsList -join ' ')"
    }
}

# Fail explicitly if the pinned user-owned plotting library cannot load.
Invoke-ResearchPython @("-c", "import contrastcolors as cc; print('contrastcolors', cc.__version__)")
Invoke-ResearchPython @("-m", "pytest", "-q")
Invoke-ResearchPython @("-m", "ruff", "check", "src", "tests", "examples", "scripts", "proximity_isomap/code")
Invoke-ResearchPython @("scripts/validate_research.py")
Invoke-ResearchPython @("scripts/validate_experiment_archive.py")

$runLabel = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
if ($Quick) { $runLabel += "-smoke" } else { $runLabel += "-full" }
Write-Host "[EXPERIMENTS] label=$runLabel seed=$Seed"
$argsList = @("proximity_isomap/code/research_runner.py", "--seed", "$Seed", "--label", $runLabel)
if ($Quick) { $argsList += "--quick" }
Invoke-ResearchPython $argsList

Invoke-ResearchPython @("scripts/validate_experiment_archive.py")
Invoke-ResearchPython @("-m", "sphinx", "-b", "html", "-W", "docs", "docs/_build/html")

Write-Host "[RESULTS] Generated figures, metrics, source provenance and updated Markdown notes."
git status --short
if ($Push) {
    # Include newly generated binary figures and NPZ arrays, not merely CSVs.
    git add -A
    if ($LASTEXITCODE -ne 0) { throw "git add failed" }
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "No new files to commit."
        return
    }
    git commit -m "Recompute EXP-001-008 with ContrastColors ($runLabel)"
    if ($LASTEXITCODE -ne 0) { throw "Commit failed." }
    git push origin main
    if ($LASTEXITCODE -ne 0) { throw "Push failed." }
    Write-Host "[PUSHED] $runLabel"
} else {
    Write-Host "No commit/push requested. Rerun with -Push to publish."
}
