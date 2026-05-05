@echo off
cd /d "C:\Users\user\WorkBuddy\Claw\乌龙指研究"
set http_proxy=http://127.0.0.1:6864
set https_proxy=http://127.0.0.1:6864
start /B /MIN pythonw.exe arbitrage_monitor.py --interval 30 --threshold 0.005 --paper > results\arbitrage_monitor.log 2>&1
echo 价差套利监控已启动! PID: %ERRORLEVEL%
echo 日志: results\arbitrage_monitor.log
