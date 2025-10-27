@echo off
:: disconnect_rdp.bat - Run as Administrator
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do (
    %windir%\System32\tscon.exe %%s /dest:console
)