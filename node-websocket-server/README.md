# Node Websocket Server

## Function
This is the websocket server for the IRC chat application. Chat messages are sent to rooms, which are then echoed back to users connected to the room. Messages are stored in mongodb.

## Vulnerabilities
There are 4 severe vulnerabilities:
- JS_EASY
- JS_MODERATE_A
- JS_MODERATE_B
- JS_MODERATE_C
- JS_HARD

## In-scope files
- `main.js`

## Exclusions
- Configuration. This challenge is focused on code, not configuration.
- Dependencies. If dependencies have vulnerabilities, don't worry about fixing them.