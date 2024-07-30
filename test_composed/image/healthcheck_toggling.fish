#!/usr/bin/env fish

sleep 1
if test (math (date +%M) % 5) -lt 3
    echo healthy
    exit 0
else
    echo unhealthy
    exit 1
end