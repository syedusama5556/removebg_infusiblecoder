@echo off
set /p id=Enter Commit Message: 
set /p version=Enter Version Number: 
git add .
git commit -m "%id%"
git tag -a v%version% -m "Version %version% release - %id%" --force
git push origin HEAD --tags
timeout 2
