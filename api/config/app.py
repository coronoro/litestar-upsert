import logging
import traceback
from typing import cast

import structlog
from advanced_alchemy.extensions.litestar import (
    AlembicAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    async_autocommit_before_send_handler,
)
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.logging.config import LoggingConfig, StructLoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.plugins.structlog import StructlogConfig
from structlog import configure
from structlog.dev import ConsoleRenderer
from structlog.processors import ExceptionPrettyPrinter, JSONRenderer, TimeStamper, StackInfoRenderer, format_exc_info
from structlog.stdlib import LoggerFactory, BoundLogger
from structlog.typing import Processor

# from litestar_saq import CronJob, QueueConfig, SAQConfig

from .base import get_settings

settings = get_settings()

compression = CompressionConfig(backend="gzip")
csrf = CSRFConfig(
    secret=settings.app.SECRET_KEY,
    cookie_secure=settings.app.CSRF_COOKIE_SECURE,
    cookie_name=settings.app.CSRF_COOKIE_NAME,
)
cors = CORSConfig(allow_origins=cast("list[str]", settings.app.ALLOWED_CORS_ORIGINS))
alchemy = SQLAlchemyAsyncConfig(
    engine_instance=settings.db.get_engine(),
    before_send_handler=async_autocommit_before_send_handler,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    alembic_config=AlembicAsyncConfig(
        version_table_name=settings.db.MIGRATION_DDL_VERSION_TABLE,
        script_config=settings.db.MIGRATION_CONFIG,
        script_location=settings.db.MIGRATION_PATH,
    ),
)


# saq = SAQConfig(
#     redis=settings.redis.client,
#     web_enabled=settings.saq.WEB_ENABLED,
#     worker_processes=settings.saq.PROCESSES,
#     use_server_lifespan=settings.saq.USE_SERVER_LIFESPAN,
#     queue_configs=[
#         QueueConfig(
#             name="system-tasks",
#             tasks=["api.domain.system.tasks.system_task", "api.domain.system.tasks.system_upkeep"],
#             scheduled_tasks=[
#                 CronJob(
#                     function="api.domain.system.tasks.system_upkeep",
#                     unique=True,
#                     cron="0 * * * *",
#                     timeout=500,
#                 ),
#             ],
#         ),
#         QueueConfig(
#             name="background-tasks",
#             tasks=["api.domain.system.tasks.background_worker_task"],
#             scheduled_tasks=[
#                 CronJob(
#                     function="api.domain.system.tasks.background_worker_task",
#                     unique=True,
#                     cron="* * * * *",
#                     timeout=300,
#                 ),
#             ],
#         ),
#     ],
# )

def error_processor(logger, method_name, event_dict):
    if event_dict.get('exc_info'):
        # If there's exception info, add it to the log message
        event_dict['error'] = event_dict['exc_info']
        del event_dict['exc_info']
    return event_dict


class CustomStackInfoRenderer(structlog.processors.StackInfoRenderer):
    def __call__(self, logger, method_name, event_dict):
        if 'stack' in event_dict:
            event_dict['stack'] = "\n".join(event_dict['stack'])
        return event_dict


log = StructlogConfig(
    structlog_logging_config=StructLoggingConfig(
        processors=[
            # structlog.stdlib.filter_by_level,  # Filter log messages by level
            # structlog.stdlib.add_logger_name,  # Add logger name to log messages
            # structlog.stdlib.add_log_level,  # Add log level to log messages
            # error_processor,  # Process errors
            # structlog.stdlib.PositionalArgumentsFormatter(),
            # CustomStackInfoRenderer(),  # Custom stack trace renderer
            # structlog.processors.format_exc_info,  # Add exception info to log messages
            structlog.processors.UnicodeDecoder(),  # Decode unicode characters
            ConsoleRenderer(),
        ],
        logger_factory=LoggerFactory(),
        wrapper_class=BoundLogger,
    )
)

# log = StructlogConfig(
#     structlog_logging_config=StructLoggingConfig(
#         processors=[
#             TimeStamper(fmt="iso"),
#             ExceptionPrettyPrinter(),
#             JSONRenderer(),
#         ],
#         logger_factory=LoggerFactory(),
#         log_exceptions="always",
#         traceback_line_limit=4,
#         standard_lib_logging_config=LoggingConfig(
#             root={"level": logging.getLevelName(settings.log.LEVEL), "handlers": ["queue_listener"]},
#             loggers={
#                 "uvicorn.access": {
#                     "propagate": False,
#                     "level": settings.log.UVICORN_ACCESS_LEVEL,
#                     "handlers": ["queue_listener"],
#                 },
#                 "uvicorn.error": {
#                     "propagate": False,
#                     "level": settings.log.UVICORN_ERROR_LEVEL,
#                     "handlers": ["queue_listener"],
#                 },
#                 "granian.access": {
#                     "propagate": False,
#                     "level": settings.log.GRANIAN_ACCESS_LEVEL,
#                     "handlers": ["queue_listener"],
#                 },
#                 "granian.error": {
#                     "propagate": False,
#                     "level": settings.log.GRANIAN_ERROR_LEVEL,
#                     "handlers": ["queue_listener"],
#                 },
#                 # "saq": {
#                 #     "propagate": False,
#                 #     "level": settings.log.SAQ_LEVEL,
#                 #     "handlers": ["queue_listener"],
#                 # },
#                 "sqlalchemy.engine": {
#                     "propagate": False,
#                     "level": settings.log.SQLALCHEMY_LEVEL,
#                     "handlers": ["queue_listener"],
#                 },
#                 "sqlalchemy.pool": {
#                     "propagate": False,
#                     "level": settings.log.SQLALCHEMY_LEVEL,
#                     "handlers": ["queue_listener"],
#                 },
#             },
#         ),
#     ),
#     middleware_logging_config=LoggingMiddlewareConfig(
#         request_log_fields=["method", "path", "path_params", "query"],
#         response_log_fields=["status_code"],
#     ),
# )
