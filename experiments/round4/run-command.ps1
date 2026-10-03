param(
    [Parameter(Mandatory)][ValidatePattern('^r0[1-6]$')][string]$Run,
    [Parameter(Mandatory)][string]$Command,
    [ValidateSet('subject', 'controller')][string]$Role = 'subject'
)
$ErrorActionPreference = 'Stop'
$trialRoot = Join-Path $PSScriptRoot ".runs/$Run"
if (-not (Test-Path -LiteralPath $trialRoot -PathType Container)) { throw 'Trial has not been prepared.' }
Push-Location -LiteralPath $trialRoot
$previousTraceTarget = $env:GIT_TRACE2_EVENT
$env:GIT_TRACE2_EVENT = Join-Path $trialRoot 'git-trace.jsonl'
[pscustomobject]@{ utc = [DateTime]::UtcNow.ToString('o'); role = $Role; command = $Command } |
    ConvertTo-Json -Compress | Add-Content -LiteralPath (Join-Path $trialRoot 'commands.jsonl') -Encoding utf8
Start-Transcript -LiteralPath (Join-Path $trialRoot 'transcript.txt') -Append | Out-Null
try {
    # The supplied command is code authored by the assigned subject, not fixture data.
    & ([scriptblock]::Create($Command))
    $commandExit = $LASTEXITCODE
} finally {
    Stop-Transcript | Out-Null
    Pop-Location
    $env:GIT_TRACE2_EVENT = $previousTraceTarget
}
if ($null -ne $commandExit) { exit $commandExit }
