@echo off
REM Script to move backup files to correct location
REM Run this after creating a backup

set WRONG_DIR=C:\VS_Code\data\backups
set CORRECT_DIR=C:\VS_Code\RWSDBv2.1\data\backups

if exist "%WRONG_DIR%\*.dump" (
    echo Moving backup files to correct location...
    move "%WRONG_DIR%\*.dump" "%CORRECT_DIR%\"
    rmdir "%WRONG_DIR%" 2>nul
    echo Done! Backups moved to %CORRECT_DIR%
) else (
    echo No backup files found in %WRONG_DIR%
)
