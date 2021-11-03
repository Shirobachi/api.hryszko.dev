#! /bin/bash
trap "sleep .5 && clear && $0 || exit 0" INT

# if parameter is given -c or --clean-up, then clean up
if [ "$1" = "-c" ] || [ "$1" = "--clean-up" ]; then
	# while docker images | grep "^<none>" | wc -l > 0 or docker ps -a | grep -v "Up " | wc -l > 1
	while [ $(docker images | grep "^<none>" | wc -l) -gt 0 ] || [ $(docker ps -a | grep -v "Up " | wc -l) -gt 1 ]; do
		# stop running containers
		docker stop $(docker ps -a -q) && 
	
		# Remove unused containers
		docker ps -a | grep -v "Up " | awk '{print $1}' | xargs docker rm -v || exit 1

		# remove unusd images
		docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi -f || exit 1
	done

	exit 0
fi

# if parameter is given -x
if [ "$1" = "-x" ]; then
	set -x 
fi

while true; do
	# Reading environment variables from .env file
	envs=""
	for i in $(seq $(cat app/.env | wc -l)); do
		left=$(cat app/.env | sed -n "$i p" | cut -d '=' -f 1)
		right=$(cat app/.env | sed -n "$i p" | cut -d '=' -f 2)

			envs="$envs -e $left=$right"
		done

		# Run the app
		docker build -t shirobachi/api.hryszko.dev . &&
		docker run -p 8000:80 $envs $(docker images | head -2 | tail -1 | awk '{print $3}') ||
		echo "Error: Cannot run the app"; exit 1
	done
fi