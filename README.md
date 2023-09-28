
# Requirements

docker
docker-compose v2 (docker compose commands)
nvidia gpu
~10GB free

# How To Run

to start the app:
`
cd app
make start
`
This will run the docker builds for the frontend and backend. The backend container ends up being pretty large with all of the 

to run backend tests
`make test_backend`

if you want to see the console output of each service, they can be run separately as follows:
`make backend`

and in a separate shell
`make frontend`


# Notes
[backend implementation inspiration](https://www.cosmicpython.com/)