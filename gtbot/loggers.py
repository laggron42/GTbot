import sys

import logging
import logging.handlers

import rich
from rich.highlighter import NullHighlighter
from rich.logging import RichHandler
from rich.style import Style
from rich.theme import Theme
from rich.traceback import PathHighlighter


def init_logger(debug: bool = False):
    log = logging.getLogger("gtbot")
    log.setLevel(logging.DEBUG)
    dpy_log = logging.getLogger("discord")
    dpy_log.setLevel(logging.WARNING)

    rich_console = rich.get_console()
    rich.reconfigure(tab_size=4)
    rich_console.push_theme(
        Theme(
            {
                "log.time": Style(dim=True),
                "logging.level.debug": Style(color="cyan"),
                "logging.level.info": Style(color="green"),
                "logging.level.warning": Style(color="yellow"),
                "logging.level.error": Style(color="red"),
                "logging.level.critical": Style(color="red", bold=True),
                "repr.number": Style(color="cyan"),
                "repr.url": Style(underline=True, italic=True, bold=False, color="blue"),
            }
        )
    )
    rich_console.file = sys.stdout
    PathHighlighter.highlights = []

    enable_rich_logging = True
    formatter = logging.Formatter(
        "[{asctime}] {levelname} {name}: {message}", datefmt="%Y-%m-%d %H:%M:%S", style="{"
    )

    # file logger
    file_handler = logging.handlers.RotatingFileHandler("gtbot.log", maxBytes=8196, backupCount=8)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    # stdout logger
    if enable_rich_logging is True:
        rich_formatter = logging.Formatter("{message}", datefmt="[%X]", style="{")
        stream_handler = RichHandler(
            rich_tracebacks=False,
            highlighter=NullHighlighter(),
        )
        stream_handler.setFormatter(rich_formatter)
    else:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
    level = logging.DEBUG if debug else logging.INFO
    stream_handler.setLevel(level)
    log.addHandler(stream_handler)
