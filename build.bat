@echo off
setlocal

pyinstaller --noconfirm -D .\src\set_wallpaper.py

:: Define the list of source directories under dist (separate them by spaces)
set "SOURCE_DIST_DIRS=.\dist\set_wallpaper"
set "SOURCE_IMAGES_DIR=.\images"
set "SOURCE_SCRIPTS_DIR=.\src\scripts"
set "DEST_DIR=.\bundle"

:: Check if the bundle directory exists, if not, create it
if not exist "%DEST_DIR%" mkdir "%DEST_DIR%"

:: Loop through each directory in SOURCE_DIST_DIRS and copy its contents
for %%D in (%SOURCE_DIST_DIRS%) do (
    xcopy "%%D\*" "%DEST_DIR%\" /E /I /Y
)

:: Check if the bundle\images directory exists, if not, create it
if not exist "%DEST_DIR%\images" mkdir "%DEST_DIR%\images"

:: Copy the contents of the images directory to bundle\images
xcopy "%SOURCE_IMAGES_DIR%\*" "%DEST_DIR%\images\" /E /I /Y

xcopy "%SOURCE_SCRIPTS_DIR%\*" "%DEST_DIR%\" /E /I /Y

echo Script execution completed.
endlocal

