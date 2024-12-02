from enum import Enum


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class Logger:
    log_level: LogLevel

    def __init__(self, log_level=LogLevel.INFO):
        self.log_level = log_level

    def log(self, log_level: LogLevel, *message: object) -> None:
        if log_level.value >= self.log_level.value:
            print(f"[{log_level.name.upper()}]:", end=" ")
            print(*message)

    def debug(self, *message: object) -> None:
        self.log(LogLevel.DEBUG, *message)

    def info(self, *message: object) -> None:
        self.log(LogLevel.INFO, *message)

    def warn(self, *message: object) -> None:
        self.log(LogLevel.WARN, *message)

    def error(self, *message: object) -> None:
        self.log(LogLevel.ERROR, *message)
