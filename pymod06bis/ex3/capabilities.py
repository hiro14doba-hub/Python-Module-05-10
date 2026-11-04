from abc import ABC, abstractmethod


class TransformCapability(ABC):
    def __init__(self) -> None:
        self._is_transformed: bool = False

    @property
    def is_transformed(self) -> bool:
        return self._is_transformed

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
