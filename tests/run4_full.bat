@echo off
chcp 65001 >nul
python src\shell1.py --vfs "tests\vfs_deep.zip" --script "tests\test_vfs_deep.txt"