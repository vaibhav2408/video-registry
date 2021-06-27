#!/bin/bash

# Creating a separate network
docker network create fampay-net_default

# Starting the elasticsearch container
docker container run -d --name elasticsearch --network fampay-net_default -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.13.2

# Building the docker image
poetry run build

echo 'Waiting for 10 seconds to let elasticsearch container start'
sleep 10

# Running the container
docker container run -d -i -t -p 5000:5000 --network fampay-net_default -v /var/keys.txt:/var/keys.txt fampay:development
