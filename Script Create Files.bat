@echo off

:choiceGlob

cls
echo 1 - Lister le contenu du dossier recherch‚
echo 2 - Renommer les fichiers
echo 3 - Cr‚ation des dossiers
echo 4 - Quitter
echo.

set /p choix=Choix : 
If %choix% EQU 1 goto filePath
If %choix% EQU 2 goto renameFiles
If %choix% EQU 3 goto mvFiles
If %choix% EQU 4 goto fin

:filePath

cls
set /p nameFile=Nom du dossier … rechercher : 
for %%i in ('dir /s %nameFile%') do set namePath=%%~dpi 
cls
cd %namePath:~0,-1%%nameFile%
dir /w
PAUSE
goto choiceGlob

:renameFiles

cls
set /p nameFileRen=Nom du dossier contenant les fichiers … renommer : 
for %%i in ('dir /s %nameFileRen%') do set namePathRen=%%~dpi 
cls
cd %namePathRen:~0,-1%%nameFileRen%
set nombre=%random%
for %%I in (*.*) do call :renameLoop "%%I" 
goto choiceGlob

:renameLoop

:inc
if exist %nombre%.* set /a nombre=%random% & goto inc
ren *.* %nombre%.*
set /a nombre=%random%
goto :eof

:mvFiles

cls
set /p nameFile=Emplacement des fichiers : 
for %%i in ('dir /s %nameFile%') do set namePath=%%~dpi 
cd %namePath:~0,-1%%nameFile%

set iter=1
md %iter%
for %%J in (*) do move %%J %iter% 

PAUSE
goto choiceGlob

:test

:fin