from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar.plugins.structlog import StructlogPlugin
from litestar_granian import GranianPlugin

from api.config import app as config
from api.server.builder import ApplicationConfigurator

structlog = StructlogPlugin(config=config.log)
alchemy = SQLAlchemyPlugin(config=config.alchemy)
granian = GranianPlugin()
app_config = ApplicationConfigurator()
