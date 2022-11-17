#!/bin/sh

docker-compose up -d

container_id=$(docker ps -aqf "name=^generate_mimic_data")
docker exec -it "$container_id" bash

