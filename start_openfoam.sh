default_container_name="of_pytorch"
container_name="${1:-$default_container_name}"
docker start $container_name
docker exec -it $container_name /bin/bash
