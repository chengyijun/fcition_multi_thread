@echo off
echo =========package start=========
rd /s/q dist
d:\venvs\py39\Scripts\pyinstaller.exe main.spec
rd /s/q build
echo =========package end=========
