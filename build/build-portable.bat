@echo off
setlocal enabledelayedexpansion

:: Configuration
set BUILD_DIR=.\
set ASSETS_DIR=assets
set ZIP_NAME=transit-route-planner-portable.zip
set ZIP_PATH=%BUILD_DIR%\%ZIP_NAME%
set TEMP_DIR=%BUILD_DIR%\temp

:: Clean previous build
echo Deleting previous ZIP file if it exists...
if exist "%ZIP_PATH%" del "%ZIP_PATH%"

echo Deleting temporary directory if it exists...
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"

:: Create temporary directories
echo Creating temporary build directory...
mkdir "%TEMP_DIR%"
mkdir "%TEMP_DIR%\output"

:: Copy static files from root
echo Copying static files...
copy /Y "..\main.py" "%TEMP_DIR%\"
copy /Y "..\set_config.py" "%TEMP_DIR%\"
copy /Y "..\requirements.txt" "%TEMP_DIR%\"
copy /Y "..\LICENCE" "%TEMP_DIR%\"

:: Copy assets directory
echo Copying assets directory...
xcopy /E /I /Y "%ASSETS_DIR%" "%TEMP_DIR%"

:: Extract python-embed
7z x "%TEMP_DIR%\python-embed.zip" -o"%TEMP_DIR%" -y
::powershell -command "Expand-Archive -LiteralPath '%TEMP_DIR%\python-embed.zip' -DestinationPath '%TEMP_DIR%' -Force"
del "%TEMP_DIR%\python-embed.zip"

:: Copy utils directory
echo Copying utils directory...
xcopy /E /I /Y "..\utils" "%TEMP_DIR%\utils"

:: Copy site-packages from .venv
echo Copying Python site-packages...
xcopy /E /I /Y "..\.venv\Lib\site-packages" "%TEMP_DIR%\python-embed\site-packages"

:: Create ZIP archive
echo Creating ZIP archive...
7z a -tzip "%ZIP_PATH%" "%TEMP_DIR%\*"
::powershell -Command "Compress-Archive -Path '%TEMP_DIR%\*' -DestinationPath '%ZIP_PATH%'"

:: Clean up temp directory
echo Removing temporary directory...
rd /s /q "%TEMP_DIR%"

echo.
echo Build complete: %ZIP_PATH%
pause