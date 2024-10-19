#!/bin/bash
# This file is out-of-scope for vulnerabilities. It runs the tests in docker for you.

# First check that the container is built. If not, build it.
docker inspect appsecchallengetests > /dev/null 2>&1 || docker build ./test/ -t appsecchallengetests

docker compose up --build -d

sleep 5

# Then run the container.
docker run -v "$(pwd)/test:/usr/src/app" --rm --network "appnetwork" appsecchallengetests "/usr/src/app/testapp.sh"

docker compose down --rmi local -t 1 -v