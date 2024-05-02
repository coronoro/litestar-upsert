from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from api.config import get_settings
from api.domain.accounts.guards import auth
from api.version import __get_package_version

current_version = __get_package_version()

settings = get_settings()
config = OpenAPIConfig(
    title=settings.app.NAME,
    version=current_version,
    components=[auth.openapi_components],
    security=[auth.security_requirement],
    use_handler_docstrings=True,
    render_plugins=[ScalarRenderPlugin()],
)
"""OpenAPI config for api.  See OpenAPISettings for configuration."""
