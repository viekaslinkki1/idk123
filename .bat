@echo off
REM Update local git repo and push changes to origin main (or master)

REM Change to the directory where this script is located
cd /d "%~dp0"

echo Pulling latest changes from remote...
git pull origin main

echo Adding all changes...
git add .

echo Enter your commit message:
set /p commitmsg=

if "%commitmsg%"=="" (
    echo Commit message cannot be empty.
    goto :eof
)

echo Committing changes...
git commit -m "%commitmsg%"

echo Pushing to remote...
git push origin main

echo Done.
pause
