Write-Host "work path: $PSScriptRoot"
$pythonPath = Join-Path -Path $PSScriptRoot -ChildPath "..\.venv\Scripts\python.exe"
$scriptPath = Join-Path -Path $PSScriptRoot -ChildPath "manage.py"
& $pythonPath $scriptPath

# INSERT INTO [dbo].[pay]([PayId],[sGameOrder],[sRoleId],[Account],[sChrName],[nExtid]\r\n,[SdkId],[ServerId], [ProductId],[Gold],[nRealGold],[Drawout],[tOrderTime])\r\nVALUES('',%s,%s,%s,%s,%d,  %s,%s, %d,%d,%d,-1,GetDate())
