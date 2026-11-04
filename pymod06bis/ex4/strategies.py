from abc import ABC, abstractmethod
from typing import Any, List
from ex3.capabilities import TransformCapability


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Any) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Any) -> List[str]:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Any) -> bool:
        return True

    def act(self, creature: Any) -> List[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Any) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Any) -> List[str]:
        if not self.is_valid(creature):
            name = getattr(creature, "name", str(creature))
            raise InvalidStrategyError(
                f"Invalid Creature '{name}' for this aggressive strategy"
            )

        return [
            creature.transform(),
            creature.attack(),
            creature.revert(),
        ]
