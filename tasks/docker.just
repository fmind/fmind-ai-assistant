# run docker tasks
[group('docker')]
docker: docker-build docker-run

# build docker image
[group('docker')]
docker-build tag="latest": package-requirements
    docker build --tag={{REPOSITORY}}:{{tag}} .

# run latest docker image
[group('docker')]
docker-run tag="latest" port="8080":
    docker run --rm --env-file=.env -p {{port}}:{{port}} {{REPOSITORY}}:{{tag}}
