# Эмулятор командной оболочки

Учебный проект по дисциплине "Конфигурационное управление".

Программа представляет собой эмулятор командной оболочки (shell) на языке
Python. Реализует базовый цикл REPL, разбор команд с поддержкой кавычек,
обработку ошибок, стартовые скрипты, работу с виртуальной файловой
системой (VFS) и основные команды UNIX-подобной оболочки.

## Автор

garkavenkoarina655-web

## Статус этапов

- [x] Этап 1 — REPL
- [x] Этап 2 — Конфигурация
- [x] Этап 3 — VFS
- [x] Этап 4 — Основные команды
- [x] Этап 5 — Дополнительные команды

## Функции и настройки

### Функции

- `parse_arguments()` — разбирает аргументы командной строки.
- `load_vfs(path)` — загружает VFS из ZIP-архива в память (словарь).
- `read_vfs_file(vfs, path)` — читает файл из VFS.
- `list_vfs_files(vfs)` — список всех файлов в VFS.
- `normalize_path(path)` — нормализует путь (убирает лишние слэши и `..`).
- `join_path(base, name)` — соединяет базовый путь и имя.
- `list_in_path(vfs, current_path)` — список файлов в текущей папке VFS.
- `list_in_path_detailed(vfs, current_path)` — список файлов с деталями (тип, размер).
- `handle_uname(cmd_args)` — обрабатывает команду `uname`.
- `handle_find(cmd_args, vfs)` — обрабатывает команду `find`.
- `handle_touch(cmd_args, vfs, current_path)` — обрабатывает команду `touch`.
- `handle_rmdir(cmd_args, vfs, current_path)` — обрабатывает команду `rmdir`.
- `read_script(path)` — читает стартовый скрипт.
- `get_prompt()` — возвращает приглашение вида `user@host:path$`.
- `handle_command(command, cmd_args, vfs, current_path)` — обрабатывает одну команду.
- `main()` — точка входа, запускает цикл REPL.

### Параметры командной строки

- `--vfs VFS` — путь к ZIP-архиву с виртуальной файловой системой.
- `--script SCRIPT` — путь к стартовому скрипту с командами.
- `-h, --help` — справка по использованию.

### Встроенные команды

- `ls [-a] [-l]` — показать файлы и папки в текущей директории VFS.
  - `-a` — показать скрытые файлы (начинающиеся с `.`).
  - `-l` — подробный формат (тип, размер).
  - `-la` или `-al` — комбинация.
- `cd [путь]` — перейти в папку внутри VFS.
  - `cd folder` — перейти в папку `folder`.
  - `cd ..` — вернуться на уровень выше.
  - `cd /` — перейти в корень VFS.
  - `cd` (без аргументов) — перейти в корень VFS.
- `cat <файл>` — прочитать файл из VFS.
- `find <шаблон>` — найти файлы в VFS по подстроке в имени.
- `uname [-a] [-s] [-r] [-h]` — информация о системе.
  - `-a` — вся информация.
  - `-s` — имя системы.
  - `-r` — версия системы.
  - `-h` — справка.
- `touch <файл>` — создать пустой файл в VFS.
  - Можно создать несколько файлов сразу: `touch a.txt b.txt`.
- `rmdir <папка>` — удалить пустую папку из VFS.
  - Удаляет только пустые папки.
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
VFS загружен. Файлы: ['hello.txt', 'readme.md', '.hidden.txt', 'folder/', 'folder/inner.txt', 'docs/', 'docs/guide.txt', 'empty/']

Ivan@DESKTOP:~$ ls
docs/
empty/
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

## Этап 4: Основные команды

### Новые команды

- `find <шаблон>` — поиск файлов по подстроке в имени.
- `uname` — информация о системе.

### Улучшенные команды

- `ls` — теперь поддерживает флаги `-a` (скрытые) и `-l` (подробно).
- `cd` — без аргументов переходит в корень VFS.

### Пример работы

```text
$ python src/shell1.py --vfs tests/vfs_multi.zip
Эмулятор оболочки
Введите 'exit' для выхода.
VFS: tests/vfs_multi.zip
VFS загружен. Файлы: ['hello.txt', 'readme.md', '.hidden.txt', 'folder/', 'folder/inner.txt', 'docs/', 'docs/guide.txt', 'empty/']

Ivan@DESKTOP:~$ uname -a
EmulatorShell 1.0 Python 3.12.5 Windows
Ivan@DESKTOP:~$ find .txt
hello.txt
folder/inner.txt
docs/guide.txt
Ivan@DESKTOP:~$ ls -la
.
..
f       24  .hidden.txt
d        0  docs/
d        0  empty/
d        0  folder/
f       22  hello.txt
f       46  readme.md
Ivan@DESKTOP:~$ exit
Пока!
```

### Тестирование команд

Для тестирования всех команд Этапа 4 используйте `run5_stage4.bat`:

```bash
tests\run5_stage4.bat
```

## Этап 5: Дополнительные команды

### Новые команды

- `touch <файл>` — создать пустой файл в VFS.
- `rmdir <папка>` — удалить пустую папку из VFS.

### Особенности

- Все изменения происходят **только в памяти** — ZIP-архив на диске не меняется.
- VFS хранится в словаре `{путь: содержимое}` — можно добавлять и удалять ключи.
- `rmdir` удаляет **только пустые** папки (как в Linux).

### Пример работы

```text
$ python src/shell1.py --vfs tests/vfs_multi.zip
Эмулятор оболочки
Введите 'exit' для выхода.
VFS: tests/vfs_multi.zip
VFS загружен. Файлы: ['hello.txt', 'readme.md', '.hidden.txt', 'folder/', 'folder/inner.txt', 'docs/', 'docs/guide.txt', 'empty/']

Ivan@DESKTOP:~$ ls
docs/
empty/
folder/
hello.txt
readme.md
Ivan@DESKTOP:~$ touch new_file.txt
Создан файл: new_file.txt
Ivan@DESKTOP:~$ ls
docs/
empty/
folder/
hello.txt
new_file.txt
readme.md
Ivan@DESKTOP:~$ rmdir empty
Удалена папка: empty/
Ivan@DESKTOP:~$ rmdir folder
Ошибка: папка не пустая: folder/
Ivan@DESKTOP:~$ exit
Пока!
```

### Тестирование команд Этапа 5

Для тестирования всех команд Этапа 5 используйте `run6_stage5.bat`:

```bash
tests\run6_stage5.bat
```

## Структура проекта

```
.
├── README.md
├── run.bat
├── .gitignore
├── src/
│   └── shell1.py
└── tests/
    ├── .gitkeep
    ├── make_vfs.py
    ├── test1.txt
    ├── test2.txt
    ├── test3.txt
    ├── test_vfs_multi.txt
    ├── test_vfs_deep.txt
    ├── test_stage4.txt
    ├── test_stage5.txt
    ├── vfs_minimal.zip
    ├── vfs_multi.zip
    ├── vfs_deep.zip
    ├── run1_no_args.bat
    ├── run2_with_vfs.bat
    ├── run3_with_script.bat
    ├── run4_full.bat
    ├── run5_stage4.bat
    ├── run6_stage5.bat
    └── run_all.bat
```

## Тестирование

Для запуска всех тестов разом:

```bash
tests\run_all.bat
```

Или через Git Bash:

```bash
cmd //c tests/run_all.bat
```

### Что тестируется

- **Test 1** — запуск без VFS (интерактив).
- **Test 2** — минимальный VFS (`vfs_minimal.zip`).
- **Test 3** — multi VFS + стартовый скрипт (`test_vfs_multi.txt`).
- **Test 4** — deep VFS + стартовый скрипт (`test_vfs_deep.txt`).
- **Test 5** — все команды Этапа 4 (`test_stage4.txt`).
- **Test 6** — все команды Этапа 5 (`test_stage5.txt`).