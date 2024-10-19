@echo off
REM This file is out-of-scope for vulnerabilities. It runs the tests in docker for you.

REM First check that the container is built. If not, build it.
docker inspect appsecchallengetests >nul 2>&1
if %ERRORLEVEL% neq 0 (
    docker build ./test/ -t appsecchallengetests
)

REM Start docker compose with build
docker compose up --build -d

REM Wait for 5 seconds
timeout /t 5 /nobreak >nul

REM Run the container
docker run -v "%cd%\test:/usr/src/app" --rm --network "appnetwork" appsecchallengetests "/usr/src/app/testapp.sh"

REM Bring down the docker-compose services and remove local images and volumes
docker compose down --rmi local -t 1 -v