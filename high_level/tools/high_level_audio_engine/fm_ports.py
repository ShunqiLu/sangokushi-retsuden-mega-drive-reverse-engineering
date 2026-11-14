"""Small explicit device contract shared by register tracing and PCM synthesis."""
from abc import ABC, abstractmethod


class FmPortDevice(ABC):
    """Actual FM port owner. Reading status must not silently move time."""

    @abstractmethod
    def read_status(self):
        raise NotImplementedError

    @abstractmethod
    def write(self, port, value):
        raise NotImplementedError
