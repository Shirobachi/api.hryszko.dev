set -x
trap "clear && $0" SIGINT

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