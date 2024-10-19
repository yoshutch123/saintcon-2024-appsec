#!/bin/bash
cd "$(dirname "$0")"

docker inspect go-remote-access >/dev/null 2>&1 || docker build . -t go-remote-access
# attaching pseudo terminal in interactive mode was only fix I could get working, --init also failed
docker run -it --rm -v ./:/var/run/go-remote-access -p 8023:8023 go-remote-access
