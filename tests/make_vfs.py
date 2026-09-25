"""Создаёт тестовый VFS-архив для эмулятора."""
import zipfile


def make_minimal_vfs(path):
    """Создаёт минимальный VFS: один файл в корне."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("hello.txt", "Привет из VFS!")

def make_multifile_vfs(path):
    """Создаёт VFS с несколькими файлами и папками."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("hello.txt", "Привет из VFS!")
        z.writestr("readme.md", "# Это README\n\nДокументация VFS.")
        z.writestr("folder/", "")                   # пустая папка
        z.writestr("folder/inner.txt", "Файл в папке folder")
        z.writestr("docs/guide.txt", "Руководство пользователя.")

def make_deep_vfs(path):
    """Создаёт VFS с 3+ уровнями вложенности."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("root.txt", "Файл в корне")
        z.writestr("level1/", "")
        z.writestr("level1/file1.txt", "Файл 1-го уровня")
        z.writestr("level1/level2/", "")
        z.writestr("level1/level2/file2.txt", "Файл 2-го уровня")
        z.writestr("level1/level2/level3/", "")
        z.writestr("level1/level2/level3/file3.txt", "Файл 3-го уровня")

if __name__ == "__main__":
    make_minimal_vfs("tests/vfs_minimal.zip")
    make_multifile_vfs("tests/vfs_multi.zip")
    make_deep_vfs("tests/vfs_deep.zip")
    print("VFS созданы:")
    print("  - tests/vfs_minimal.zip")
    print("  - tests/vfs_multi.zip")
    print("  - tests/vfs_deep.zip")