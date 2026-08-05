#!/bin/sh

# 1. Определяем путь к папке, где лежит сам скрипт
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 2. Проверка на наличие .git
if [ ! -d ".git" ]; then
    echo "Error: Current directory is not a git repository."
    echo 'Please initialize a repository with "git init -b main" or move to an existing one.'
    exit 1
fi

# 3. Основная логика проверки git-task
check_alias_and_exit() {
    # 3.1. Проверка конфига на наличие алиаса
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

# 3. Проверка файла в .git
if [ -f "./.git/git-task" ]; then
    check_alias_and_exit
fi

# 4. Проверка файлов в папке со скриптом (дистрибутив)
FOUND_FILE=""
FOUND_COUNT=0
FOUND_LIST=""

# 4.1. Ищем только три конкретных релиза
for file in "git-task-linux" "git-task-macos-arm64" "git-task-macos-intel"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        FOUND_FILE="$SCRIPT_DIR/$file"
        FOUND_COUNT=$((FOUND_COUNT + 1))
        if [ -z "$FOUND_LIST" ]; then
            FOUND_LIST="$file"
        else
            FOUND_LIST="$FOUND_LIST, $file"
        fi
    fi
done

# 4.2. Если найден ровно ОДИН файл — копируем его
if [ "$FOUND_COUNT" -eq 1 ]; then
    cp "$FOUND_FILE" "./.git/git-task"
    chmod +x "./.git/git-task"
    check_alias_and_exit
# Если найдено НЕСКОЛЬКО файлов — выводим ошибку
elif [ "$FOUND_COUNT" -gt 1 ]; then
    echo "Error: Multiple release files found in '$SCRIPT_DIR': $FOUND_LIST"
    echo "Please delete the inappropriate releases and keep only the one matching your OS."
    exit 1
fi

# 5. Ошибка, если ни один из файлов не найден
echo "Error: No release files ('git-task-linux', 'git-task-macos-arm64', or 'git-task-macos-intel') found in '$SCRIPT_DIR'."
echo "Please download the appropriate release from https://github.com/asquebay/Git-task-manager/releases and follow the README instructions."
exit 1
