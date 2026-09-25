@echo off
echo    RUN ALL TESTS
echo.

echo === Test 1: no args ===
call tests\run1_no_args.bat
echo.

echo === Test 2: with minimal VFS ===
call tests\run2_with_vfs.bat
echo.

echo === Test 3: with multi VFS and script ===
call tests\run3_with_script.bat
echo.

echo === Test 4: with deep VFS and script ===
call tests\run4_full.bat
echo.

echo    ALL TESTS COMPLETED
pause