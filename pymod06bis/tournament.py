from typing import List, Tuple

from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory,
)
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def run_tournament(
    opponents: List[Tuple[CreatureFactory, BattleStrategy]]
) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            print("* Battle *")
            factory_a, strategy_a = opponents[i]
            factory_b, strategy_b = opponents[j]

            creature_a = factory_a.create_base()
            creature_b = factory_b.create_base()

            print(creature_a.describe())
            print("VS.")
            print(creature_b.describe())
            print("now fight!")

            try:
                for line in strategy_a.act(creature_a):
                    print(line)
                for line in strategy_b.act(creature_b):
                    print(line)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    normal_strategy = NormalStrategy()
    aggressive_strategy = AggressiveStrategy()

    print("Tournament 0 (basic)")
    print("[(Flameling+Normal), (Shiftling+Aggressive)]")
    run_tournament([
        (flame_factory, normal_strategy),
        (transform_factory, aggressive_strategy),
    ])

    print("Tournament 1 (error)")
    print("[(Shiftling+Aggressive), (Flameling+Aggressive)]")
    run_tournament([
        (transform_factory, aggressive_strategy),
        (flame_factory, aggressive_strategy),
    ])


if __name__ == "__main__":
    main()
