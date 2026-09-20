import os
import socket
import getpass
import shlex
import argparse

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

def get_prompt():
    """Возвращает приглашение для ввода команд."""
    user = getpass.getuser()
    host = socket.gethostname()
    name = os.getcwd()
    home = os.path.expanduser("~")

    if name == home:
        name = "~"

    return f"{user}@{host}:{name}$ "

def handle_command(command, cmd_args):
    """Обрабатывает одну команду. Возвращает True, если надо выйти."""
    if command == "exit":
        print("Пока!")
        return True
    elif command == "ls":
        print(f"[ls] вызвана с аргументами: {cmd_args}")
    elif command == "cd":
        print(f"[cd] вызвана с аргументами: {cmd_args}")
    else:
        print(f"Команда не найдена: {command}")
    return False

def main():
    """Точка входа. Запускает цикл REPL."""
    args = parse_arguments()
    print(" Эмулятор оболочки ")
    print("Введите 'exit' для выхода.")
    if args.vfs:
        print(f"VFS: {args.vfs}")
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
            if handle_command(args_list[0], args_list[1:]):
                return

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

        if handle_command(args_list[0], args_list[1:]):
            break
if __name__ == "__main__":
    main()