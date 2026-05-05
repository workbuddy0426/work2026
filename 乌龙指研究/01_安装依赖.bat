@echo off
echo ========================================
echo 小乌：安装乌龙指研究所需依赖
echo ========================================
echo.

C:\Users\user\hermes-agent\venv\Scripts\python.exe -m pip install pandas numpy akshare -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ========================================
echo 安装完成！
echo ========================================
pause