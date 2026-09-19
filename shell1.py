import os
import socket
import getpass
import shlex

def get_prompt():
    user = getpass.getuser()
    host = socket.gethostname()
    name = os.getcwd()
    home = os.path.expanduser("~")

    if name == home:
        name = "~"

    return f"{user}@{host}:{name}$ "


def main():
    print(" Эмулятор оболочки ")
    print("Введите 'exit' для выхода.")
    print()

    while True:
        try:
            line = input(get_prompt())
        except (KeyboardInterrupt, EOFError):
            print("\nПока!")
            break

        if not line.strip():
            continue

        try:
            args = shlex.split(line)
        except ValueError as e:
            print(f"Ошибка разбора: {e}")
            continue

        if not args:
            continue

        command = args[0]
        cmd_args = args[1:]

        if command == "exit":
            print("Пока!")
            break
        elif command == "ls":
            print(f"[ls] вызвана с аргументами: {cmd_args}")
        elif command == "cd":
            print(f"[cd] вызвана с аргументами: {cmd_args}")
        else:
            print(f"Команда не найдена: {command}")


if __name__ == "__main__":
    main()