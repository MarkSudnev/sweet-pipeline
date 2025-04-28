from pathlib import Path

import requests
from requests import Response
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage


class TestApp:

    docker_context = Path(__file__).parent.parent
    docker_image = DockerImage(path=docker_context, tag="data-source-test")
    docker_container: DockerContainer = ...

    @classmethod
    def setup_method(cls):
        cls.docker_image.build()
        cls.docker_container = DockerContainer(str(cls.docker_image)).with_exposed_ports(8091)
        cls.docker_container.start()

    @classmethod
    def teardown_method(cls):
        cls.docker_container.stop()
        cls.docker_image.remove()

    def test_returns_ok_when_query_is_present_and_correct(self):
        host = self.docker_container.get_container_host_ip()
        port = self.docker_container.get_exposed_port(8091)
        url = f"http://{host}:{port}/api/v1/data?q=hello"
        print(f"URL = {url}")
        response: Response = requests.get(url)
        assert response.ok
