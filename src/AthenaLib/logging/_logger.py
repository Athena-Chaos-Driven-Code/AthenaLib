# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
import enum
import concurrent.futures
from dataclasses import dataclass, field
from typing import Callable

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
error_type = lambda obj: f"the following did not inherit from expected AthenaLoggerType: {obj}"
error_logger = lambda obj: f"the following did not inherit from expected AthenaLogger: {obj}"

class LoggerLevels(enum.StrEnum):
    TRACK = enum.auto()
    DEBUG = enum.auto()
    WARN = enum.auto()
    ERROR = enum.auto()

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class AthenaLogger(ABC):
    enable_track:bool = True
    enable_debug:bool = True
    enable_warning:bool = True
    enable_error:bool = True

    _pool_executor: concurrent.futures.ProcessPoolExecutor = field(init=False, default_factory=lambda:concurrent.futures.ProcessPoolExecutor(max_workers=1))
    _logger_entered:bool = field(init=False, default=False)
    _buffer:list[tuple[LoggerLevels, str|enum.StrEnum, str|None]] = field(init=False, default_factory=list)

    def __enter__(self):
        self._logger_entered = True
        for level, section, text in self._buffer:
            self.log(level, section, text)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Makes sure the pool executor is shot down,
        #   else the process will keep to exist and errors might occur
        self._pool_executor.shutdown()

    # ------------------------------------------------------------------------------------------------------------------
    # - Abstract Features that need to be implemented -
    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def log(self, level:LoggerLevels, section:str|enum.StrEnum, text:str|None):
        pass

    def log_track(self, section:str|enum.StrEnum, text:str|None=None):
        """
        Simple log command that is meant for data that needs to be tracked while in development mode.
        Should be disabled once sufficient data has been gathered throughout development
        """
        if self.enable_track:
            self.log(level=LoggerLevels.TRACK, section=section, text=text)

    def log_debug(self, section:str|enum.StrEnum, text:str|None=None):
        """
        Simple log command for debug data
        """
        if self.enable_debug:
            self.log(level=LoggerLevels.DEBUG, section=section, text=text)

    def log_warning(self, section:str|enum.StrEnum, text:str|None=None):
        """
        Simple log command for Warnings
        """
        if self.enable_warning:
            self.log(level=LoggerLevels.WARN, section=section, text=text)

    def log_error(self, section:str|enum.StrEnum, text:str|None=None):
        """
        Simple log command for Errors
        """
        if self.enable_error:
            self.log(level=LoggerLevels.ERROR, section=section, text=text)



