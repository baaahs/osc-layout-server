#!/usr/bin/env bash

docker build . --tag=baaahs/layout-server:latest
docker push baaahs/layout-server:latest
