# Эмулятор командной оболочки

Учебный проект по дисциплине "Конфигурационное управление".

Программа представляет собой эмулятор командной оболочки (shell) на языке
Python. Реализует базовый цикл REPL, разбор команд с поддержкой кавычек,
обработку ошибок, стартовые скрипты и работу с виртуальной файловой
системой (VFS).

## Автор

garkavenkoarina655

## Статус этапов

- [x] Этап 1 — REPL
- [x] Этап 2 — Конфигурация
- [x] Этап 3 — VFS

## Функции и настройки

### Функции

- `parse_arguments()` — разбирает аргументы командной строки.
- `load_vfs(path)` — загружает VFS из ZIP-архива.
- `read_vfs_file(vfs, path)` — читает файл из VFS.
- `list_vfs_files(vfs)` — список всех файлов в VFS.
- `normalize_path(path)` — нормализует путь (убирает лишние слэши и `..`).
- `join_path(base, name)` — соединяет базовый путь и имя.
- `list_in_path(vfs, current_path)` — список файлов в текущей папке VFS.
- `read_script(path)` — читает стартовый скрипт.
- `get_prompt()` — возвращает приглашение вида `user@host:path$`.
- `handle_command(command, cmd_args, vfs, current_path)` — обрабатывает одну команду.
- `main()` — точка входа, запускает цикл REPL.

### Параметры командной строки

- `--vfs VFS` — путь к ZIP-архиву с виртуальной файловой системой.
- `--script SCRIPT` — путь к стартовому скрипту с командами.
- `-h, --help` — справка по использованию.

### Встроенные команды

- `ls` — показать файлы и папки в текущей директории VFS.
- `cd <путь>` — перейти в папку внутри VFS.
  - `cd folder` — перейти в папку `folder`.
  - `cd ..` — вернуться на уровень выше.
  - `cd /` — перейти в корень VFS.
- `cat <файл>` — прочитать файл из VFS.
- `exit` — завершить работу эмулятора.

## Сборка и запуск

### Требования

- Python 3.10+

### Запуск в интерактивном режиме

```bash
python src/shell1.py
```

### Запуск со стартовым скриптом

```bash
python src/shell1.py --script tests/test1.txt
```

### Запуск с VFS

```bash
python src/shell1.py --vfs tests/vfs_multi.zip
```

### Запуск с VFS и скриптом

```bash
python src/shell1.py --vfs tests/vfs_multi.zip --script tests/test_vfs_multi.txt
```

### Запуск через скрипт run.bat (Windows)

```bash
run.bat
```

### Справка

```bash
python src/shell1.py --help
```

## Примеры использования

### Пример 1: базовые команды

```text
$ python src/shell1.py
Эмулятор оболочки
Введите 'exit' для выхода.

Ivan@DESKTOP:~$ ls -la
[ls] вызвана с аргументами: ['-la']
Ivan@DESKTOP:~$ cd "Моя папка"
[cd] вызвана с аргументами: ['Моя папка']
Ivan@DESKTOP:~$ exit
Пока!
```

### Пример 2: обработка ошибок

```text
Ivan@DESKTOP:~$ qwerty
Команда не найдена: qwerty
Ivan@DESKTOP:~$ echo "незакрытая кавычка
Ошибка разбора: No closing quotation
```

### Пример 3: стартовый скрипт

Файл `tests/test1.txt`:

```text
# Тестовый скрипт 1

ls
cd /home
ls -la
```

Запуск:

```bash
python src/shell1.py --script tests/test1.txt
```

Вывод:

```text
Эмулятор оболочки
Введите 'exit' для выхода.
Стартовый скрипт: tests/test1.txt

Ivan@DESKTOP:~$ ls
[ls] вызвана с аргументами: []
Ivan@DESKTOP:~$ cd /home
[cd] вызвана с аргументами: ['/home']
Ivan@DESKTOP:~$ ls -la
[ls] вызвана с аргументами: ['-la']
Ivan@DESKTOP:~$ _
```

## Этап 3: Виртуальная файловая система (VFS)

### Что такое VFS

VFS — это ZIP-архив, который эмулятор читает прямо в памяти, не распаковывая на диск. Внутри архива — файлы и папки, которые эмулятор видит как настоящую файловую систему.

### Пример работы с VFS

```text
$ python src/shell1.py --vfs tests/vfs_multi.zip
Эмулятор оболочки
Введите 'exit' для выхода.
VFS: tests/vfs_multi.zip
VFS загружен. Файлы: ['hello.txt', 'readme.md', 'folder/', 'folder/inner.txt', 'docs/guide.txt']

Ivan@DESKTOP:~$ ls
docs/
folder/
hello.txt
readme.md
Ivan@DESKTOP:~$ cd folder
[cd] перешли в /folder
Ivan@DESKTOP:~$ ls
inner.txt
Ivan@DESKTOP:~$ cat inner.txt
Файл в папке folder
Ivan@DESKTOP:~$ cd ..
[cd] перешли в /
Ivan@DESKTOP:~$ exit
Пока!
```

### Тестовые VFS

В папке `tests/` есть три VFS-архива:

- `vfs_minimal.zip` — минимальный (один файл).
- `vfs_multi.zip` — с несколькими файлами и папками.
- `vfs_deep.zip` — с 3 уровнями вложенности.

### Генерация VFS

VFS-архивы создаются скриптом `tests/make_vfs.py`:

```bash
python tests/make_vfs.py
```

### Тестирование VFS

Для тестирования всех вариантов VFS используйте `run_all.bat`:

```bash
tests\run_all.bat
```