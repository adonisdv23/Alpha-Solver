#!/bin/sh
curl -s -H "X-API-Key: dev-secret" -H "Content-Type: application/json" \
    -d '{"query":"hi","strategy":"react"}' \
    http://localhost:8000/v1/solve | jq .
