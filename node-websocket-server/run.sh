#!/bin/bash
docker inspect node-websocket-server > /dev/null 2>&1 || docker build . -t node-websocket-server
docker run -v ./:/var/run/go-remote-access -p 8801:8801 node-websocket-server
