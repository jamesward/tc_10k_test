import pytest
import main
from testcontainers.core.container import DockerContainer


@pytest.mark.asyncio
async def test_all():
    # todo: no way to set pull policy yet
    docker_container = DockerContainer("ghcr.io/jamesward/easyracer").with_exposed_ports(8080)
    with docker_container as easyracer:
        port = int(easyracer.get_exposed_port(8080))

        # todo: can't find the right way to wait on the container being ready
        import time
        time.sleep(2)

        #@wait_container_is_ready()
        async def connected():
            result1 = await main.scenario1(port)
            assert result1 == "right"

            result3 = await main.scenario3(port)
            assert result3 == "right"
        await connected()
