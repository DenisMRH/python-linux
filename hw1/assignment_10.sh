#!/bin/bash

echo "Original PATH: $PATH"

ORIGINAL_PATH=$PATH

export PATH="$PATH:$HOME"
echo "New PATH with HOME: $PATH"

INTERNAL_SCRIPT="$HOME/assignment_10_internal_script.sh"
echo 'echo "Content of internal script"' > "$INTERNAL_SCRIPT"

chmod u+x "$INTERNAL_SCRIPT"

echo "Running internal script..."
assignment_10_internal_script.sh

export PATH=$ORIGINAL_PATH
echo "Restored PATH: $PATH"

echo "Running again after restoring PATH..."
assignment_10_internal_script.sh

# Получилось ли запустить второй раз? 
# Ответ: Нет.
# Потому что после восстановления PATH система больше не ищет исполняемые 
# файлы в домашней директории. Теперь, чтобы его запустить, нужно указывать полный 
# или относительный путь.