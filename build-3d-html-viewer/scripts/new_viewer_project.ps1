param(
  [Parameter(Mandatory=$true)]
  [string]$ProductTitle,

  [Parameter(Mandatory=$true)]
  [string]$StepPath,

  [Parameter(Mandatory=$true)]
  [string]$OutputDirectory,

  [string]$Description = "",
  [string]$SourceNotice = "",
  [string]$OutputSlug = "",
  [string]$PdfPath = "",
  [string]$NativePath = "",
  [string[]]$GroundImagePaths = @(),
  [switch]$UseDefaultSmtLayoutFloor,
  [string]$DefaultSmtLayoutImageUrl = "https://ph.smthelp.com/images/2025/06/06/SMT-line-Single-Lane-Layout-1.png"
)

$ErrorActionPreference = "Stop"

function Convert-ToSlug {
  param([string]$Value)
  $slug = $Value.ToLowerInvariant() -replace '[^a-z0-9]+','-'
  $slug = $slug.Trim('-')
  if ([string]::IsNullOrWhiteSpace($slug)) { return "product-interactive-3d-viewer" }
  return $slug
}

$skillRoot = Split-Path -Parent $PSScriptRoot
$template = Join-Path $skillRoot "assets\viewer-template"
if (!(Test-Path -LiteralPath $template)) {
  throw "Template not found: $template"
}
if (!(Test-Path -LiteralPath $StepPath)) {
  throw "STEP source not found: $StepPath"
}

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
Get-ChildItem -LiteralPath $template -Force | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination $OutputDirectory -Recurse -Force
}

$assetDir = Join-Path $OutputDirectory "assets"
New-Item -ItemType Directory -Force -Path $assetDir | Out-Null

$stepName = "model" + [IO.Path]::GetExtension($StepPath)
Copy-Item -LiteralPath $StepPath -Destination (Join-Path $assetDir $stepName) -Force

$pdfName = $null
if ($PdfPath -and (Test-Path -LiteralPath $PdfPath)) {
  $pdfName = "source-3d-pdf" + [IO.Path]::GetExtension($PdfPath)
  Copy-Item -LiteralPath $PdfPath -Destination (Join-Path $assetDir $pdfName) -Force
}

$nativeName = $null
if ($NativePath -and (Test-Path -LiteralPath $NativePath)) {
  $nativeName = "source-native" + [IO.Path]::GetExtension($NativePath)
  Copy-Item -LiteralPath $NativePath -Destination (Join-Path $assetDir $nativeName) -Force
}

$groundImages = @()
$groundIndex = 1

if ($UseDefaultSmtLayoutFloor) {
  $defaultGroundName = "ground-smt-line-single-lane-layout.png"
  $defaultGroundPath = Join-Path $assetDir $defaultGroundName
  Invoke-WebRequest -Uri $DefaultSmtLayoutImageUrl -OutFile $defaultGroundPath -UseBasicParsing
  $groundImages += [PSCustomObject]@{
    label = "SMT single-lane layout floor image"
    file = $defaultGroundName
    mime = "image/png"
    sourceUrl = $DefaultSmtLayoutImageUrl
  }
  $groundIndex += 1
}

foreach ($groundPath in $GroundImagePaths) {
  if ($groundPath -and (Test-Path -LiteralPath $groundPath)) {
    $extension = [IO.Path]::GetExtension($groundPath)
    if ([string]::IsNullOrWhiteSpace($extension)) { $extension = ".png" }
    $groundName = "ground-image-$groundIndex$extension"
    Copy-Item -LiteralPath $groundPath -Destination (Join-Path $assetDir $groundName) -Force
    $mime = switch ($extension.ToLowerInvariant()) {
      ".jpg" { "image/jpeg" }
      ".jpeg" { "image/jpeg" }
      ".webp" { "image/webp" }
      ".gif" { "image/gif" }
      default { "image/png" }
    }
    $groundImages += [PSCustomObject]@{
      label = "Ground image $groundIndex"
      file = $groundName
      mime = $mime
      sourceUrl = ""
    }
    $groundIndex += 1
  }
}

$configPath = Join-Path $OutputDirectory "viewer-config.json"
$config = Get-Content -LiteralPath $configPath -Encoding UTF8 | ConvertFrom-Json
$config.productTitle = $ProductTitle
$config.description = $(if ($Description) { $Description } else { "Interactive 3D visual reference for $ProductTitle, prepared as a WordPress-compatible Southern Machinery product page." })
$config.sourceNotice = $(if ($SourceNotice) { $SourceNotice } else { "This interactive 3D view helps customers and engineers review product geometry, clearance, and integration concept before final compatibility confirmation." })
$config.outputSlug = $(if ($OutputSlug) { Convert-ToSlug $OutputSlug } else { Convert-ToSlug $ProductTitle })
$config.screenshotName = $config.outputSlug
$config.source.step = $stepName
$config.source.pdf = $pdfName
$config.source.native = $nativeName
if ($groundImages.Count -gt 0) {
  $config.groundImages = @($groundImages)
}

$config | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $configPath -Encoding UTF8

[PSCustomObject]@{
  Project = (Resolve-Path -LiteralPath $OutputDirectory).Path
  Config = $configPath
  Step = $stepName
  Pdf = $pdfName
  Native = $nativeName
  GroundImages = @($groundImages | ForEach-Object { $_.file })
  NextCommands = "npm.cmd install; npm.cmd run all; npm.cmd run verify"
}
