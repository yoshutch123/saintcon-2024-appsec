# Go Remote Access Server

## Function
A remote administration program that allows a user to authenticate and run arbitrary commands on the host.

## Vulnerabilities
There are 2 severe vulnerabilities:
- GO-EASY
- GO-HARD

## In-scope files
- main.go

## Exclusions
- Rate-limiting. Usually one would implement this with a separate piece of software, and that's just a lot of work for this challenge.
- Constant-time string compare for password.
- Post-auth command injection. That is the entire point of this program.
- Clear-text password storage. Yes, it is a problem. However, a rando on the internet cannot abuse this in any meaningful way without compromising the host in the first place. You are focused on the code, not the config.