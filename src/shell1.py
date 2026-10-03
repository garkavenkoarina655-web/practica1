import os
import socket
import getpass
import shlex
import argparse
import zipfile


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки"
    )
    parser.add_argument(
        "--vfs",
        help="Путь к физическому расположению VFS",
        default=None
    )
    parser.add_argument(
        "--script",
        help="Путь к стартовому скрипту",
        default=None
    )
    return parser.parse_args()


def load_vfs(path):
    """Загружает VFS из ZIP-архива в память. Возвращает словарь или None."""
    if path is None:
        return None
    try:
        with zipfile.ZipFile(path, "r") as z:
            vfs = {}
            for name in z.namelist():
                vfs[name] = z.read(name)
            return vfs
    except FileNotFoundError:
        print(f"Ошибка: файл VFS не найден: {path}")
        return None
    except zipfile.BadZipFile:
        print(f"Ошибка: неверный формат VFS (не ZIP): {path}")
        return None
    except Exception as e:
        print(f"Ошибка загрузки VFS: {e}")
        return None


def read_vfs_file(vfs, path):
    """Читает файл из VFS. Возвращает текст или None."""
    if vfs is None:
        print("VFS не загружен.")
        return None
    try:
        content = vfs[path]
        return content.decode("utf-8")
    except KeyError:
        print(f"Файл не найден в VFS: {path}")
        return None
    except UnicodeDecodeError:
        print(f"Не удалось декодировать файл (не текст?): {path}")
        return None
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None


def read_script(path):
    """Читает стартовый скрипт и возвращает список команд."""
    commands = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                commands.append(line)
    except FileNotFoundError:
        print(f"Ошибка: файл скрипта не найден: {path}")
    except Exception as e:
        print(f"Ошибка чтения скрипта: {e}")
    return commands


def list_vfs_files(vfs):
    """Возвращает список файлов в VFS. Или None, если VFS не загружен."""
    if vfs is None:
        print("VFS не загружен.")
        return None
    try:
        return list(vfs.keys())
    except Exception as e:
        print(f"Ошибка чтения списка файлов: {e}")
        return None


def normalize_path(path):
    """Приводит путь к виду /a/b/c без лишних слэшей."""
    if not path:
        return "/"
    parts = []
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/" + "/".join(parts)


def join_path(base, name):
    """Соединяет базовый путь и имя, возвращает нормализованный путь."""
    if base == "/":
        return normalize_path("/" + name)
    return normalize_path(base + "/" + name)


def list_in_path(vfs, current_path):
    """Возвращает список файлов и папок в current_path (только 1-й уровень)."""
    if vfs is None:
        return None
    all_files = list(vfs.keys())
    prefix = "" if current_path == "/" else current_path.lstrip("/") + "/"
    items = set()
    for file in all_files:
        if not file.startswith(prefix):
            continue
        rest = file[len(prefix):]
        if not rest:
            continue
        first = rest.split("/")[0]
        if "/" in rest:
            first += "/"
        items.add(first)
    return sorted(items)


def list_in_path_detailed(vfs, current_path):
    """Возвращает список записей в current_path с деталями.

    Каждая запись — словарь: name, is_dir, size.
    """
    if vfs is None:
        return None
    all_files = list(vfs.keys())
    prefix = "" if current_path == "/" else current_path.lstrip("/") + "/"
    items = {}
    for file in all_files:
        if not file.startswith(prefix):
            continue
        rest = file[len(prefix):]
        if not rest:
            continue
        first = rest.split("/")[0]
        is_dir = "/" in rest
        name = first + "/" if is_dir else first
        if name in items:
            continue
        if is_dir:
            items[name] = {"name": name, "is_dir": True, "size": 0}
        else:
            try:
                size = len(vfs[(file)])
            except Exception:
                size = 0
            items[name] = {"name": name, "is_dir": False, "size": size}
    return [items[k] for k in sorted(items.keys())]


def get_prompt():
    """Возвращает приглашение для ввода команд."""
    user = getpass.getuser()
    host = socket.gethostname()
    name = os.getcwd()
    home = os.path.expanduser("~")

    if name == home:
        name = "~"

    return f"{user}@{host}:{name}$ "


def handle_uname(cmd_args):
    """Обрабатывает команду uname. Возвращает True, если нужно вывести help."""
    import platform #даёт информацию о системе и Python

    system_name = "EmulatorShell"
    version = "1.0"
    python_version = platform.python_version()
    os_name = platform.system()

    if not cmd_args:
        print(system_name)
    elif cmd_args[0] == "-a":
        print(f"{system_name} {version} Python {python_version} {os_name}")
    elif cmd_args[0] == "-s":
        print(system_name)
    elif cmd_args[0] == "-r":
        print(version)
    elif cmd_args[0] in ("-h", "--help"):
        print("Использование: uname [опции]")
        print("  -a         вся информация")
        print("  -s         имя системы")
        print("  -r         версия системы")
    else:
        print(f"uname: неизвестная опция: {cmd_args[0]}")
    return False


def handle_find(cmd_args, vfs):
    """Обрабатывает команду find. Ищет файлы по подстроке в имени."""
    if vfs is None:
        print("VFS не загружен.")
        return False

    if not cmd_args:
        print("Использование: find <шаблон>")
        print("  Пример: find .txt — найти все файлы с .txt в имени")
        return False

    pattern = cmd_args[0]
    try:
        all_files = list(vfs.keys())
    except Exception as e:
        print(f"Ошибка чтения VFS: {e}")
        return False

    found = []
    for file in all_files:
        if file.endswith("/"):
            continue
        if pattern in file:
            found.append(file)

    if not found:
        print(f"Ничего не найдено по шаблону: {pattern}")
    else:
        for file in found:
            print(file)
    return False

def handle_touch(cmd_args, vfs, current_path):
    """Обрабатывает команду touch. Создаёт пустой файл в VFS."""
    if vfs is None:
        print("VFS не загружен.")
        return False

    if not cmd_args:
        print("Использование: touch <файл>")
        return False

    for name in cmd_args:
        file_path = join_path(current_path, name).lstrip("/")

        if file_path in vfs:
            print(f"Файл уже существует: {file_path}")
            continue

        if file_path.endswith("/"):
            print(f"Ошибка: это папка, а не файл: {file_path}")
            continue

        vfs[file_path] = b""
        print(f"Создан файл: {file_path}")

    return False

def handle_rmdir(cmd_args, vfs, current_path):
    """Обрабатывает команду rmdir. Удаляет пустую папку из VFS."""
    if vfs is None:
        print("VFS не загружен.")
        return False

    if not cmd_args:
        print("Использование: rmdir <папка>")
        return False

    for name in cmd_args:
        dir_path = join_path(current_path, name).lstrip("/")

        if not dir_path.endswith("/"):
            dir_path += "/"

        if dir_path not in vfs:
            print(f"Папка не найдена: {dir_path}")
            continue

        prefix = dir_path
        is_empty = True
        for key in vfs.keys():
            if key == dir_path:
                continue
            if key.startswith(prefix):
                is_empty = False
                break

        if not is_empty:
            print(f"Ошибка: папка не пустая: {dir_path}")
            continue

        del vfs[dir_path]
        print(f"Удалена папка: {dir_path}")

    return False

def handle_command(command, cmd_args, vfs, current_path):
    """Обрабатывает одну команду. Возвращает True, если надо выйти."""
    if command == "exit":
        print("Пока!")
        return True
    elif command == "ls":
        show_all = "-a" in cmd_args or "-la" in cmd_args or "-al" in cmd_args
        long_format = "-l" in cmd_args or "-la" in cmd_args or "-al" in cmd_args

        items = list_in_path_detailed(vfs, current_path)
        if items is None:
            print("VFS не загружен.")
        else:
            if show_all:
                print(".")
                print("..")
            for item in items:
                name = item["name"]
                if not show_all and name.startswith("."):
                    continue
                if long_format:
                    kind = "d" if item["is_dir"] else "f"
                    size = item["size"]
                    print(f"{kind} {size:>8}  {name}")
                else:
                    print(name)
    elif command == "cd":
        if not cmd_args:
            new_path = "/"
        else:
            target = cmd_args[0]
            if target.startswith("/"):
                new_path = normalize_path(target)
            else:
                new_path = join_path(current_path, target)
        print(f"[cd] перешли в {new_path}")
        return new_path
    elif command == "cat":
        if not cmd_args:
            print("Использование: cat <файл>")
            return False
        file_path = join_path(current_path, cmd_args[0]).lstrip("/")
        content = read_vfs_file(vfs, file_path)
        if content is not None:
            print(content)
    elif command == "uname":
        handle_uname(cmd_args)
    elif command == "find":
        handle_find(cmd_args, vfs)
    elif command == "touch":
        handle_touch(cmd_args, vfs, current_path)
    elif command == "rmdir":
        handle_rmdir(cmd_args, vfs, current_path)
    else:
        print(f"Команда не найдена: {command}")
    return False

def main():
    """Точка входа. Запускает цикл REPL."""
    args = parse_arguments()
    current_path = "/"
    print(" Эмулятор оболочки ")
    print("Введите 'exit' для выхода.")
    vfs = None
    if args.vfs:
        print(f"VFS: {args.vfs}")
        vfs = load_vfs(args.vfs)
        if vfs is None:
            print("Не удалось загрузить VFS. Продолжаю без него.")
        else:
            print(f"VFS загружен. Файлы: {list(vfs.keys())}")
    if args.script:
        print(f"Стартовый скрипт: {args.script}")
    print()

    if args.script:
        commands = read_script(args.script)
        for command in commands:
            print(f"{get_prompt()}{command}")
            try:
                args_list = shlex.split(command)
            except ValueError as e:
                print(f"Ошибка разбора: {e}")
                continue
            if not args_list:
                continue
            result = handle_command(args_list[0], args_list[1:], vfs, current_path)
            if result is True:
                return
            elif isinstance(result, str):
                current_path = result

    while True:
        try:
            line = input(get_prompt())
        except (KeyboardInterrupt, EOFError):
            print("\nПока!")
            break

        if not line.strip():
            continue

        try:
            args_list = shlex.split(line)
        except ValueError as e:
            print(f"Ошибка разбора: {e}")
            continue

        if not args_list:
            continue

        result = handle_command(args_list[0], args_list[1:], vfs, current_path)
        if result is True:
            break
        elif isinstance(result, str):
            current_path = result


if __name__ == "__main__":
    main()