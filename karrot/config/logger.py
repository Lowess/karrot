#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging."""

import structlog
from logging.config import dictConfig

HAS_COLORAMA = False
try:
    import colorama

    HAS_COLORAMA = True
except ImportError:
    pass


class Logger:
    """Logger configuration."""

    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")

    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
    ]

    @classmethod
    def init(cls, level="DEBUG"):
        """Initialize application logging."""
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "plain": {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(colors=HAS_COLORAMA),
                        "foreign_pre_chain": cls.pre_chain,
                    },
                    "colored": {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(colors=HAS_COLORAMA),
                        "foreign_pre_chain": cls.pre_chain,
                    },
                    "json": {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.processors.JSONRenderer(),
                        "foreign_pre_chain": cls.pre_chain,
                    },
                },
                "handlers": {
                    "default": {
                        "level": level,
                        "class": "logging.StreamHandler",
                        "formatter": "colored",
                    },
                },
                "loggers": {
                    "": {"handlers": ["default"], "level": level, "propagate": True},
                },
            }
        )

        structlog.configure(
            processors=[
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                cls.timestamper,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            context_class=structlog.threadlocal.wrap_dict(dict),
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
