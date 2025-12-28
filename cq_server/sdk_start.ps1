Write-Host "work path: $PSScriptRoot"
$pythonPath = Join-Path -Path $PSScriptRoot -ChildPath ".venv\Scripts\python.exe"
$scriptPath = Join-Path -Path $PSScriptRoot -ChildPath "manage.py"
& $pythonPath $scriptPath

