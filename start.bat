echo off
start /min cmd /k python gameHTTPServer.py
start /min cmd /c python gameWebSocketServer.py
cd C:\Windows\System32
Taskkill /IM chrome.exe /F
start chrome -fullscreen "http://192.168.178.65:8000/"
start chrome "http://192.168.178.65:8010/"