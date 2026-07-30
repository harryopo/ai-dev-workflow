@echo off
REM 关闭 GitHub 代理（用于 git push，push 需要直连认证）
git config --global --unset url.https://ghproxy.net/https://github.com/.insteadof 2>nul
echo [OK] GitHub 代理已关闭（直连模式）
