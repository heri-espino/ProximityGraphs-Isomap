# Import original EXP-010/EXP-011 archive source, outputs, figures and complete notes.
# Put the two previously generated ZIPs into Downloads; call -Push after review.
[CmdletBinding()]
param(
  [string]$Exp010Archive = "$HOME\Downloads\ProximityGraphs-Isomap-EXP-010.zip",
  [string]$Exp011Archive = "$HOME\Downloads\ProximityGraphs-Isomap-EXP-011.zip",
  [switch]$Push
)
$ErrorActionPreference="Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ((git branch --show-current).Trim() -ne "main") { throw "Switch to main." }
if (git status --porcelain) { throw "Working tree must be clean; commit/stash first." }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "git pull failed" }
foreach ($zip in @($Exp010Archive,$Exp011Archive)) {
  if (-not (Test-Path -LiteralPath $zip -PathType Leaf)) { throw "Archive not found: $zip" }
}
$tmp=Join-Path ([IO.Path]::GetTempPath()) ("pg_import_"+[guid]::NewGuid().ToString("N"))
New-Item -Path $tmp -ItemType Directory | Out-Null
try {
  $jobs=@(
    @{ Archive=$Exp010Archive; Slug="010-radius_density_and_rings"; Test="test_exp_010.py"; Min=4 },
    @{ Archive=$Exp011Archive; Slug="011-isomap_baselines"; Test="test_exp_011.py"; Min=8 }
  )
  foreach ($j in $jobs) {
    $unpack=Join-Path $tmp $j.Slug
    Expand-Archive -LiteralPath $j.Archive -DestinationPath $unpack
    foreach ($kind in @("code","results","figures","notes")) {
      $src=Join-Path $unpack ("proximity_isomap\"+$kind+"\"+$j.Slug)
      $dst=Join-Path "proximity_isomap" ($kind+"\"+$j.Slug)
      if (-not (Test-Path -LiteralPath $src)) { throw "Missing source folder: $src" }
      New-Item -Path $dst -ItemType Directory -Force | Out-Null
      Get-ChildItem -LiteralPath $src -Recurse -File | Where-Object {
        $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and $_.Extension -ne '.pyc'
      } | ForEach-Object {
        $rel=$_.FullName.Substring($src.Length).TrimStart('\','/')
        $target=Join-Path $dst $rel
        New-Item -Path (Split-Path $target -Parent) -ItemType Directory -Force | Out-Null
        if ((Test-Path -LiteralPath $target) -and $kind -ne "notes") {
          $same=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash -eq (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
          if (-not $same) { throw "Refusing to overwrite a different frozen/source file: $target" }
        } else { Copy-Item -LiteralPath $_.FullName -Destination $target -Force }
      }
    }
    $srcTest=Join-Path $unpack ("tests\"+$j.Test)
    $dstTest=Join-Path "tests" $j.Test
    if (-not (Test-Path -LiteralPath $srcTest)) { throw "Missing test: $srcTest" }
    if (-not (Test-Path -LiteralPath $dstTest)) { Copy-Item -LiteralPath $srcTest -Destination $dstTest }
    $note=Join-Path "proximity_isomap\notes" ($j.Slug+"\README.md")
    $links=[regex]::Matches((Get-Content -LiteralPath $note -Raw),'!\[[^\]]*\]\((\.\./\.\./figures/[^)]+)\)')
    if ($links.Count -lt $j.Min) { throw "Original note does not embed enough figures: $note" }
    foreach ($link in $links) {
      $p=[IO.Path]::GetFullPath((Join-Path (Split-Path $note -Parent) $link.Groups[1].Value))
      if (-not (Test-Path -LiteralPath $p)) { throw "Broken image link: $p" }
    }
    $runDir=Join-Path "proximity_isomap\figures" ($j.Slug+"\runs")
    $png=@(Get-ChildItem -LiteralPath $runDir -Recurse -File -Filter "*.png").Count
    $svg=@(Get-ChildItem -LiteralPath $runDir -Recurse -File -Filter "*.svg").Count
    if ($png -lt $j.Min -or $svg -lt $j.Min) { throw "Missing original PNG/SVG gallery" }
    Write-Host "[VERIFIED LOCAL] $($j.Slug): $png PNG, $svg SVG"
  }
  conda run --no-capture-output -n proximity-isomap python -m pytest tests/test_exp_010.py tests/test_exp_011.py -q
  if ($LASTEXITCODE -ne 0) { throw "Experiment tests failed" }
  git add -A -- proximity_isomap/code/010-radius_density_and_rings proximity_isomap/code/011-isomap_baselines proximity_isomap/results/010-radius_density_and_rings proximity_isomap/results/011-isomap_baselines proximity_isomap/figures/010-radius_density_and_rings proximity_isomap/figures/011-isomap_baselines proximity_isomap/notes/010-radius_density_and_rings proximity_isomap/notes/011-isomap_baselines tests/test_exp_010.py tests/test_exp_011.py
  git diff --cached --check
  if ($LASTEXITCODE -ne 0) { throw "Bad staged changes" }
  git diff --cached --stat
  if ($Push) {
    if (-not (git diff --cached --name-only)) { Write-Host "Nothing to commit"; return }
    git commit -m "Publish original EXP-010/011 code, numerical results and figures"
    if ($LASTEXITCODE -ne 0) { throw "Commit failed" }
    git push origin main
    if ($LASTEXITCODE -ne 0) { throw "Push failed" }
    Write-Host "[PUSHED COMMIT] $(git rev-parse HEAD)"
  } else { Write-Host "Staged only. Review, then use -Push to publish." }
} finally {
  Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
