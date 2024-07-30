## Install wheel

```shell
docker build \
    --tag container-health-exporter/builder/install-wheel:latest \
    -f builder/Dockerfile \
    --target install-wheel \
        .

docker run -it --rm \
    --name container-health-exporter-builder \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --mount type=bind,src=(path resolve ./artifacts),dst=/artifacts \
        container-health-exporter/builder/install-wheel:latest
```



## Make deb

```shell
docker build \
    --tag container-health-exporter/builder/make-deb:latest \
    -f builder/Dockerfile \
    --target make-deb \
        .

docker run -it --rm \
    --name container-health-exporter-builder \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --mount type=bind,src=(path resolve ./artifacts),dst=/artifacts \
        container-health-exporter/builder/make-deb:latest
```



## Copy deb

```shell
docker build \
    --tag container-health-exporter/builder/copy-deb:latest \
    -f builder/Dockerfile \
    --target copy-deb \
        .

docker run -it --rm \
    --name container-health-exporter-builder \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --mount type=bind,src=(path resolve ./artifacts),dst=/artifacts \
        container-health-exporter/builder/copy-deb:latest
```