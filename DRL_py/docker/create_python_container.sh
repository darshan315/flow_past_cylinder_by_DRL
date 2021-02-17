username="$USER"
user="$(id -u)"
default_image="darsh3/python_drl:latest"
image="${1:-$default_image}"
default_container_name="python_drl"
container_name="${2:-$default_container_name}"

docker run -it -d --name $container_name \
  --user=${user} \
  -e USER=${username} \
  --workdir="$HOME" \
  --volume="$(pwd):$HOME" \
  --volume="/etc/group:/etc/group:ro" \
  --volume="/etc/passwd:/etc/passwd:ro" \
  --volume="/etc/shadow:/etc/shadow:ro" \
  --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
  $image
