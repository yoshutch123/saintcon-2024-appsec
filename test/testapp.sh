#!/bin/bash
# This file is out-of-scope for vulnerabilities. PLEASE USE DOCKER K THX BYE
export irc=$(dig +short irc.local)

pytest unit/ --disable-warnings