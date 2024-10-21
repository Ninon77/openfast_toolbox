@echo off
color 0b
setlocal enabledelayedexpansion
title create png's from *.outb files

set /A _Anzahl=1
set exe=python.exe
set pythonScript=..\figures.py
set var_color=.\variable_color_list.json

for %%f IN (..\..\..\data\example_files\*.outb) DO (
    rem Construct the corresponding .png file name
    set "pngFile=%%~nf.png"
    echo !pngFile!
    rem Check if the .png file does not exist
    if not exist "!pngFile!" (
	echo.
	echo !_Anzahl! processing file: %%f
	%exe% %pythonScript% -l %var_color% -i %%f
	set /A _Anzahl+=1
    ) else (
        echo Found corresponding .png file for: %%f
    )
)
pause