@echo off
set /p id=Enter Commit Message: 
git add .
git commit -m "%id%"
git push origin Head
timeout 2
