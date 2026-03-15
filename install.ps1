# install.ps1 — Install skill generator skills to another project or globally
#
# Usage:
#   install.ps1 -Target C:\other\project    # Install to a project's .claude/skills/
#   install.ps1 -Global                      # Install to ~/.claude/skills/
#
# Skills are sourced from this project's .claude/skills/ directory.

param(
    [string]$Target,
    [switch]$Global
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceDir = Join-Path $ScriptDir ".claude" "skills"

# Determine install directory
if ($Global) {
    $InstallDir = Join-Path $HOME ".claude" "skills"
} elseif ($Target) {
    $InstallDir = Join-Path $Target ".claude" "skills"
} else {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  install.ps1 -Target C:\other\project   # Install to a project" -ForegroundColor White
    Write-Host "  install.ps1 -Global                     # Install globally" -ForegroundColor White
    exit 1
}

$Skills = @("validate-skill", "generate-skill", "improve-skill")

Write-Host "`nInstalling skills to $InstallDir ...`n" -ForegroundColor Cyan

foreach ($Skill in $Skills) {
    $Source = Join-Path $SourceDir $Skill
    $TargetPath = Join-Path $InstallDir $Skill

    if (-not (Test-Path $Source)) {
        Write-Host "  [SKIP] $Skill - source not found at $Source" -ForegroundColor Yellow
        continue
    }

    # Create target directory
    if (-not (Test-Path $TargetPath)) {
        New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    }

    # Copy SKILL.md
    Copy-Item (Join-Path $Source "SKILL.md") -Destination $TargetPath -Force

    # Copy references/ if exists
    $RefsSource = Join-Path $Source "references"
    if (Test-Path $RefsSource) {
        $RefsTarget = Join-Path $TargetPath "references"
        if (-not (Test-Path $RefsTarget)) {
            New-Item -ItemType Directory -Path $RefsTarget -Force | Out-Null
        }
        Copy-Item (Join-Path $RefsSource "*") -Destination $RefsTarget -Force
    }

    # Copy scripts/ if exists
    $ScriptsSource = Join-Path $Source "scripts"
    if (Test-Path $ScriptsSource) {
        $ScriptsTarget = Join-Path $TargetPath "scripts"
        if (-not (Test-Path $ScriptsTarget)) {
            New-Item -ItemType Directory -Path $ScriptsTarget -Force | Out-Null
        }
        Copy-Item (Join-Path $ScriptsSource "*") -Destination $ScriptsTarget -Force
    }

    Write-Host "  [OK] $Skill" -ForegroundColor Green
}

Write-Host "`nDone! Installed skills:" -ForegroundColor Cyan
foreach ($Skill in $Skills) {
    Write-Host "  /$Skill" -ForegroundColor White
}
Write-Host "`nRestart Claude Code to pick up new skills.`n" -ForegroundColor Yellow
