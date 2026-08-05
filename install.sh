#!/bin/sh

# Определяем путь к папке, где лежит сам скрипт
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Проверка на наличие .git
if [ ! -d ".git" ]; then
    echo "Error: Current directory is not a git repository."
    echo 'Please initialize a repository with "git init -b main" or move to an existing one.'
    exit 1
fi

# 2. Основная логика проверки git-task
check_alias_and_exit() {
    # 2.1. Проверка конфига на наличие алиаса
    if grep -q 'task = ./.git/git-task' ".git/config" 2>/dev/null; then
        echo "Git task manager is already initialized in this project."
        echo "Usage: git task -h"
        exit 0
    else
        git config alias.task '!.git/git-task'
        echo "Git task manager initialized successfully."
        echo "Usage: git task -h"
        exit 0
    fi
}

# 2. Проверка файла в .git
if [ -f "./.git/git-task" ]; then
    check_alias_and_exit
fi

# 3. Проверка файла в папке со скриптом (дистрибутив)
DIST_FILE="$SCRIPT_DIR/dist/git-task"
if [ -f "$DIST_FILE" ]; then
    # 3.1. Копирование и переход к проверке алиаса
    cp "$DIST_FILE" "./.git/git-task"
    # Даём права на исполнение, чтобы git мог запустить файл
    chmod +x "./.git/git-task"
    check_alias_and_exit
fi

# 4. Ошибка, если файл не найден
echo "Error: File './dist/git-task' not found in '$SCRIPT_DIR'."
echo "Please download the release from https://github.com/asquebay/Git-task-manager/releases and follow the README instructions."
exit 1
