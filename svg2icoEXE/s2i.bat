@echo off
title SVG to ICO
set directoryPath=%~dp0
set exePath=svg2ico
MODE 65,30
echo.
echo -----------------------------------------------------------------
echo 			     SVG2ICO
echo -----------------------------------------------------------------
echo.
set argPath=%1
for %%i in (%argPath%) do set parentDir=%%~dpi
set outPath=%parentDir%icons
if not exist %outPath% (
    mkdir %outPath%
)
if exist "%argPath%\" (
    %exePath% -fd %argPath% -o %outPath%
) else (
    %exePath% -f %argPath% -o %outPath%
)
pause