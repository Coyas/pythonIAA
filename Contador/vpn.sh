@echo off
:loop
    nordvpn c
    timeout /t 72 >nul  :: Espera 72 segundos (1,20 minutos = 1 minuto + 12 segundos)
    goto loop

