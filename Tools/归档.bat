@echo off
setlocal enabledelayedexpansion
for %%i in (%*) do (
  "C:\Program Files\7-Zip\7z.exe" a -mx7 "%%~nxi.7z" "%%~i"
)
pause