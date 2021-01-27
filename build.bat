@echo off
cls
start /min cmd /k python src/gameHTTPServer.py
start /min cmd /c python src/gameWebSocketServer.py
taskkill /IM chrome.exe /F
start chrome -fullscreen "http://192.168.178.65:8000/"
start chrome "http://192.168.178.65:8010/"
