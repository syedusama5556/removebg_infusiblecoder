@echo off

REM Build the Docker image
docker compose -f docker-compose.cpu.yml build && 

REM Push the Docker image to Docker Hub
docker push syedusama5556/removebg_infusiblecoder:latest
