# Docker Instructions

The Docker environment is configured with a Dockerfile, which defines the popsim image, and a docker-compose.yaml, which maps a local directory to a volume in the container when the image is run.

To set up and use the environment to run populationsim:

1. Build the popsim image with docker compose: `docker-compose up`

2. Run the popsim image interactively with bash: `docker-compose run popsim bash`

3. Navigate to the model directory: `cd ps_taz` or `cd ps_taz_2050`

4. (Only need to do once) If you need to create the seed files from the PUMS data: `python make-seed-from-pums.py`

5. Run populationsim: `python run_populationsim.py`

6. Rename variables per model spec: `python update-variable-names.py`

## Common Problems

1. If the populationsim script exits with 'Killed', you may not have allocated sufficient memory to your docker containers. Try allocating more memory: https://forums.docker.com/t/how-to-increase-memory-size-that-is-available-for-a-docker-container/78483

2. In order to create the seed data, you need to download the PUMS data. See `populationsim-taz/download-PUMS`. 
