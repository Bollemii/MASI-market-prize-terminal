#!/bin/bash

docker build -t loot_game --file deploy.dockerfile .

docker run -it --name loot_game --rm --volume $PWD/data:/app/data loot_game
