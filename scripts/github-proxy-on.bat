@echo off
REM 开启 GitHub 代理加速（用于 git clone / git pull）
git config --global url."https://ghproxy.net/https://github.com/".insteadOf "https://github.com/"
echo [OK] GitHub 代理已开启 (ghproxy.net)
