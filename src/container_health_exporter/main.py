#!/usr/bin/env python3

import docker.models
import docker.models.containers
from prometheus_client import CollectorRegistry, Gauge, Info, generate_latest
import docker

registry = CollectorRegistry()
namespace = "containers_health"

exporter_version = Info(
    "exporter_version",
    "Exporter version",
    namespace=namespace,
    registry=registry,
)

container_id_name_labels = ["id", "name"]
containers_state_status = Gauge(
    "containers_state",
    "Container's status; gauge values: 1 for \"runnning\", 2 for \"paused\", 4 for \"exited\"",
    [*container_id_name_labels],
    namespace=namespace,
    registry=registry
)
containers_state_health = Gauge(
    "containers_state_health",
    "Container healthyness;  gauge values: 1 for when container has no healtcheck, 2 for \"starting\", 4 for \"healthy\" and 8 for \"unhealthy\"",
    [*container_id_name_labels],
    namespace=namespace,
    registry=registry
)


def __map_status_to_gauge_value(state: dict) -> int:
    match state["Status"]:
        case "running":
            return 1
        case "paused":
            return 2
        case "exited":
            return 4
        case _:
            raise ValueError(f"Unexpected status \"{state["Status"]}\".")

def __map_health_status_to_gauge_value(state: dict) -> int:
    health_state = "unchecked"
    if "Health" in state:
        health_state = state["Health"]["Status"]
    match health_state:
        case "unchecked":
            return 1
        case "starting":
            return 2
        case "healthy":
            return 4
        case "unhealthy":
            return 8
        case _:
            raise ValueError(f"Unexpected health state \"{health_state}\".")

def __collect_container_metric(client: docker.DockerClient, container: docker.models.containers.Container):
    state = client.api.inspect_container(container.id)["State"]

    containers_state_status.labels(
        id=container.id,
        name=container.name
        ).set(__map_status_to_gauge_value(state))

    containers_state_health.labels(
        id=container.id,
        name=container.name
        ).set(__map_health_status_to_gauge_value(state))


def __collect_containers_metrics():
    d = docker.from_env()
    containers = d.containers.list(all=True)
    for container in containers:
        try:
            __collect_container_metric(d, container)
        except Exception as e:
            raise RuntimeError(f"Failed to collect metrics for container \"{container.id}\".") from e
        
def print_containers_metrics():
    exporter_version.info({"version": "0.7.0"})

    __collect_containers_metrics()
    print(generate_latest(registry).decode(), end="")


if __name__ == '__main__':
    print_containers_metrics()
