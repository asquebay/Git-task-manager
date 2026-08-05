@echo off
chcp 65001 > nul

:: 1. Определяем путь к папке, где лежит сам скрипт
set "SCRIPT_DIR=%~dp0"

:: 2. Проверка на наличие .git
if not exist .git\ (
    echo Error: Current directory is not a git repository.
    echo Please initialize a repository with "git init -b main" or move to an existing one.
    goto end
)

:: 3. Проверка файла в .git
if exist ".git\git-task.exe" (
    goto check_alias_and_exit
)

:: 4. Проверка файла в папке со скриптом (дистрибутив)
set "DIST_FILE=%SCRIPT_DIR%git-task-windows.exe"
if exist "%DIST_FILE%" (
    :: 4.1. Копирование и переход к проверке алиаса
    copy /Y "%DIST_FILE%" ".git\git-task.exe" > nul
    goto check_alias_and_exit
)

:: 5. Ошибка, если файл не найден
echo Error: File './git-task-windows.exe' not found in '%SCRIPT_DIR%'.
echo Please download the release from https://github.com/asquebay/Git-task-manager/releases and follow the README instructions.
goto end

:check_alias_and_exit
:: Ищем строку task в конфигурационном файле .git/config
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
