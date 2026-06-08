@echo off
setlocal enabledelayedexpansion
for %%i in (%*) do (
  set a=%%i
  rd /s /q "%%~i\_internal\tcl8"
  rd /s /q "%%~i\_internal\_tk_data\images"
  rd /s /q "%%~i\_internal\_tk_data\msgs"
  rd /s /q "%%~i\_internal\_tcl_data\encoding"
  rd /s /q "%%~i\_internal\_tcl_data\http1.0"
  rd /s /q "%%~i\_internal\_tcl_data\msgs"
  rd /s /q "%%~i\_internal\_tcl_data\opt0.4"
  rd /s /q "%%~i\_internal\_tcl_data\tzdata"
  del /f /q "%%~i\_internal\_bz2.pyd"
  del /f /q "%%~i\_internal\_decimal.pyd"
  del /f /q "%%~i\_internal\_hashlib.pyd"
  del /f /q "%%~i\_internal\_lzma.pyd"
  del /f /q "%%~i\_internal\_socket.pyd"
  del /f /q "%%~i\_internal\libcrypto-1_1.dll"
  del /f /q "%%~i\_internal\select.pyd"
)
pause