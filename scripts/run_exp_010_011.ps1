# Run the original research questions natively. No ZIP downloads or Ruff.
# .\scripts\run_exp_010_011.ps1 -Quick              # smoke only
# .\scripts\run_exp_010_011.ps1 -RequireUmap       # full; require real UMAP
[CmdletBinding()]
param([switch]$Quick,[switch]$RequireUmap,[int]$Seed=20261018)
$ErrorActionPreference="Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$label=(Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
if ($Quick) { $label += "-smoke" } else { $label += "-full" }
Write-Host "[RUN LABEL] $label"
Write-Host "[EXP-010] Cylinder, rings, graph components and fixed-scale VR H1"
$args010=@("proximity_isomap/code/010-radius_density_and_rings/run.py","--label",$label)
if ($Quick) { $args010+="--quick" }
conda run --no-capture-output -n proximity-isomap python @args010
if ($LASTEXITCODE -ne 0) { throw "EXP-010 failed; results have NOT been published." }
Write-Host "[EXP-011] PCA, global and componentwise kNN Isomap, t-SNE and UMAP"
$args011=@("proximity_isomap/code/011-isomap_baselines/run.py","--label",$label,"--seed","$Seed")
if ($Quick) { $args011+="--quick" }
if ($RequireUmap) { $args011+="--require-umap" }
conda run --no-capture-output -n proximity-isomap python @args011
if ($LASTEXITCODE -ne 0) { throw "EXP-011 failed; inspect saved files before proceeding." }
Write-Host "[COMPLETE] Outputs were generated on THIS machine with label $label"
Write-Host "Results: proximity_isomap/results/{010-radius_density_and_rings,011-isomap_baselines}/runs/$label"
Write-Host "Figures: proximity_isomap/figures/{010-radius_density_and_rings,011-isomap_baselines}/runs/$label"
Write-Host "Nothing has been pushed automatically. Inspect and git add/commit/push after completion."
