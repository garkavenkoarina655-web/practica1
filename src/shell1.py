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
    """Загружает VFS из ZIP-архива. Возвращает объект ZipFile или None."""
    if path is None:
        return None
    try:
        vfs = zipfile.ZipFile(path, "r")
        return vfs
    except FileNotFoundError:
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
        content = vfs.read(path)
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
        return vfs.namelist()
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
    all_files = vfs.namelist()
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

def get_prompt():
    """Возвращает приглашение для ввода команд."""
    user = getpass.getuser()
    host = socket.gethostname()
    name = os.getcwd()
    home = os.path.expanduser("~")

    if name == home:
        name = "~"

    return f"{user}@{host}:{name}$ "

def handle_command(command, cmd_args, vfs, current_path):
    """Обрабатывает одну команду. Возвращает True, если надо выйти."""
    if command == "exit":
        print("Пока!")
        return True
    elif command == "ls":
        items = list_in_path(vfs, current_path)
        if items is None:
            print("VFS не загружен.")
        else:
            for item in items:
                print(item)
    elif command == "cd":
        if not cmd_args:
            print("Использование: cd <путь>")
            return False
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
            print(f"VFS загружен. Файлы: {vfs.namelist()}")
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