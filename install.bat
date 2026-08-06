@echo off
chcp 65001 > nul

REM 1. Get script directory path
set "SCRIPT_DIR=%~dp0"

REM 2. Check for .git directory
if not exist .git\ (
    echo error: Current directory is not a git repository.
    echo Please initialize a repository with "git init -b main" or move to an existing one.
    goto end
)

REM 3. Check if target file already exists in .git
if exist ".git\git-task.exe" (
    goto check_alias_and_exit
)

REM 4. Check if source file exists in script directory
set "DIST_FILE=%SCRIPT_DIR%git-task-windows.exe"
if exist "%DIST_FILE%" (
    REM 4.1. Copy file and proceed to alias validation
    copy /Y "%DIST_FILE%" ".git\git-task.exe" > nul
    goto check_alias_and_exit
)

REM 5. Error if file not found
echo error: File './git-task-windows.exe' not found in '%SCRIPT_DIR%'.
echo Please download the release from https://github.com/asquebay/Git-task-manager/releases and follow the README instructions.
goto end

:check_alias_and_exit
REM 6. Search for alias in .git/config
findstr /C:"task = !.git/git-task.exe" .git\config > nul 2>&1
if %errorlevel% equ 0 (
    echo Git task manager is already initialized in this project.
    echo Usage: git task -h
) else (
    git config alias.task "!.git/git-task.exe"
    echo Git task manager initialized successfully.
    echo Usage: git task -h
)
goto end

:end
echo.
echo Script execution finished. Press any key to exit...
pause > nul
