# SAINTCON 2024 AppSec Challenge

**Please read this README thoroughly. It will answer many of your questions.**

## Basic info
This web application consists of several smaller components, each written in a different langauge. Hopefully you will encounter a language you are familiar with.

More information about each service can be found in their respective README files. These will contain really, really helpful information, like the number of vulns in the service and what is in or out of scope.

It should be noted that for the purposes of this challenge, the server is intended to run on `localhost` OR `irc.local`. You should treat these as possible hostnames for the server.

## Prerequisites
- Python
- Docker
- a few gigs of disk space for docker images
- A Linux OS, or a willingness to deal with any possible issues that may arise on Windows/Mac when running tests locally


## Running
Services run in docker on localhost. Don't expose ports or run code natively, you don't want to run vulnerable code on your host machine.

You can visit the vulnerable website at `http://localhost:42101`.

To run all services:

```
docker compose up --build -d
```

To run a specific service:
```
docker-compose up --build -d <service name from docker-compose.yml>
```

To stop services:

```
docker compose down
```

To rebuild a specific service (for faster iteration):
```
docker compose up --build <service name from docker-compose.yml>
```
For example, `docker compose up --build java-api` would restart/rebuild my Java service without restarting all other services.

To complete nuke all running services:
```
docker compose down -t 1 -v --remove-orphans --rmi local
```

It is a good idea to read through `docker-compose.yml` to understand which services run on which ports, in case you'd like to test them directly instead of through the nginx proxy.

It's also a good idea to periodically run `docker system prune --volumes` to remove dangling containers/images and save on disk space.



## Testing

Services must be stopped before running unit tests.

Linux (recommended) or Mac:

`./runtests.sh`

Windows:

`.\runtests.bat` or `.\runtests.ps1`

Note that the local tests my be flaky on Windows, and we didn't test at all on Mac. Everything should still *work* fine with writing code and running the web application though.

## Submitting
Run `python3 make_package.py` and submit the resulting `appsec-submission.zip` to https://appsec.saintcon.community. You'll need to create an account first.

Submissions that do not pass unit tests will not be scored for vulnerabilities.

Files you change outside of those listed in scope (as referenced in README files and fully enumerated in `allowed_files.txt`) will not be included in your submission. Limit your changes to those files.