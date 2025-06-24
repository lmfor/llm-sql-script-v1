import subprocess
import time
import docker
import pytest

TEST_IMAGE_NAME = "tool-test-image"
TEST_CONTAINER_NAME = "tool-test-container"
PORT = "8000"


@pytest.fixture(autouse=True, scope="module")
def BUILD_TEST_IMAGE():
    try:
        dc = docker.DockerClient(base_url="unix://var/run/docker.sock")
    except Exception as e:
        try:
            dc = docker.DockerClient(base_url="npipe:////./pipe/docker_engine")
        except Exception as e:
            pytest.exit("Docker engine is not running on this system " + str(e), 3)

    result = dc.images.build(
        path=".",
        dockerfile="Dockerfile",
        tag=TEST_IMAGE_NAME,
    )
    print("Docker build output:", result)

    try:
        dc.containers.run(
            TEST_IMAGE_NAME,
            detach=True,
            name=TEST_CONTAINER_NAME,
            ports={f"{PORT}/tcp": PORT},
        )
    except Exception as e:
        print("Could not start unittest container " + str(e))
        dc.containers.get(TEST_CONTAINER_NAME).stop()
        dc.containers.get(TEST_CONTAINER_NAME).remove()
        dc.containers.run(
            TEST_CONTAINER_NAME,
            detach=True,
            name=TEST_CONTAINER_NAME,
            ports={f"{PORT}/tcp": PORT},
        )

    time.sleep(20)
    yield
    try:
        dc.containers.get(TEST_CONTAINER_NAME).stop()
        dc.containers.get(TEST_CONTAINER_NAME).remove()
    except Exception as e:
        pytest.exit("Could not remove unittest container " + str(e), 3)
