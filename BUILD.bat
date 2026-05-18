@echo off
title A compilar AutoGreenClicker...
echo.
echo  Instalando dependencias...
pip install pyautogui pillow numpy pystray pyinstaller --quiet

echo.
echo  A compilar .exe (pode demorar 1-2 minutos)...
pyinstaller --onefile --noconsole --icon=icon.ico --name="AutoGreenClicker" --clean AutoGreenClicker.py

echo.
if exist dist\AutoGreenClicker.exe (
    echo  PRONTO! O teu exe esta em:  dist\AutoGreenClicker.exe
    echo  Copia-o para onde quiseres e faz pin na barra de tarefas.
    explorer dist
) else (
    echo  Algo correu mal. Verifica os erros acima.
)
pause
