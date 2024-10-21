# This file is out-of-scope for vulnerabilities. It runs the tests in docker for you.

# First check that the container is built. If not, build it.
$containerExists = docker inspect appsecchallengetests > $null 2>&1
if (-not $?) {
    docker build ./test/ -t appsecchallengetests
}

# Start docker compose with build
docker compose up --build -d

# Wait for 5 seconds
Start-Sleep -Seconds 10

# Run the container
docker run -v "$(pwd)/test:/usr/src/app" --rm --network "appnetwork" appsecchallengetests "/bin/bash" "/usr/src/app/testapp.sh"

# Bring down the docker compose services and remove local images and volumes
docker compose down --rmi local -t 1 -v
