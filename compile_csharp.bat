@echo off
REM compile_csharp.bat
echo Компиляция C# ядра в DLL...
cd WifiCore_CS
dotnet build -c Release
if %errorlevel% equ 0 (
    echo Копирование WifiCore.dll в корень проекта...
    copy bin\Release\net481\WifiCore.dll ..\
    echo Готово! DLL скомпилирована успешно.
) else (
    echo Ошибка компиляции! Проверьте наличие .NET SDK.
    pause
)
cd ..
pause