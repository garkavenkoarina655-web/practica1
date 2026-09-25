@echo off
chcp 65001 >nul
python src\shell1.py --vfs "tests\vfs_multi.zip" --script "tests\test_vfs_multi.txt"