import requests
import pytest
import schemathesis
from testcontainers.core import container
from testcontainers.core import waiting_utils


class VaultContainer(container.DockerContainer):
    VAULT_PORT = 8200

    @property
    def vault_address(self) -> str:
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self.VAULT_PORT)
        return f"http://{host}:{port}"

    @property
    def openapi_url(self) -> str:
        return f"{self.vault_address}/v1/sys/internal/specs/openapi"

    @waiting_utils.wait_container_is_ready(requests.ConnectionError)
    def wait_for(self):
        resp = requests.head(
            url=f"{self.vault_address}/v1/sys/health",
        )
        resp.raise_for_status()

    def start(self):
        super().start()
        self.wait_for()
        return self


@pytest.fixture(name="vault_root_token")
def _vault_root_token():
    """static root token used when interacting with vault"""
    return "root"


@pytest.fixture(name="vault_container")
def _vault_container(vault_root_token):
    vault = (
        VaultContainer(image="vault")
        .with_env("VAULT_DEV_ROOT_TOKEN_ID", vault_root_token)
        .with_exposed_ports(VaultContainer.VAULT_PORT)
        .with_kwargs(cap_add=["IPC_LOCK"])
    )
    vault.start()
    yield vault
    vault.stop()


@pytest.fixture(name="vault_openapi_schema")
def _vault_schema(vault_container, vault_root_token):
    schema = schemathesis.from_uri(
        uri=vault_container.openapi_url,
        headers={"X-Vault-Token": vault_root_token},
        base_url=f"{vault_container.vault_address}/v1",
    )

    @schema.auth.register()
    class Auth:

        def get(self, context):
            return vault_root_token

        def set(self, case, data, context):
            case.headers = {"X-Vault-Token": data}

    return schema
