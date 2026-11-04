from abc import ABC, abstractmethod
from typing import Any, Union, Sequence


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0
        self._total_procces: int = 0

    @abstractmethod
    def validate(self, data: Any):
        pass

    @abstractmethod
    def ingest(self, data: Any):
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data output")
        current_rank = self._rank
        self._rank += 1
        return current_rank, self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list) and data:
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        else:
            return False

    def ingest(self, data: Union[int, float,
                                 Sequence[Union[int, float]]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._total_procces += 1
                self._storage.append(str(item))
        else:
            self._total_procces += 1
            self._storage.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and data:
            return all(
                isinstance(x, str)for x in data
            )
        return False

    def ingest(self, data: Union[str, list[str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._total_procces += 1
                self._storage.append(item)
        else:
            self._total_procces += 1
            self._storage.append(data)


class LogProcessor(DataProcessor):
    def is_valid_log(self, data: Any) -> bool:
        if isinstance(data, dict):
            return "log_level" in data and "log_message" in data
        return False

    def validate(self, data: Any) -> bool:
        if self.is_valid_log(data):
            return True
        if isinstance(data, list) and data:
            return all(
                self.is_valid_log(x)for x in data
            )
        return False
    def ingest(
            self, data: Union[dict[str, str], list[dict[str, str]]]) -> None:

        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._total_procces += 1
                msg = f"{item['log_level']}: {item['log_message']}"
                self._storage.append(msg)
        else:
            self._total_procces += 1
            msg = f"{data['log_level']}: {data['log_message']}"
            self._storage.append(msg)


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []
        self._total_procces: int = 0

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            handlet = False
            for proc in self.processors:
                if proc.validate(item):
                    proc.ingest(item)
                    self._total_procces += 1
                    handlet = True
                    break
            if not handlet:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{item}")

    def print_processors_stats(self) -> None:
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            print(f"{proc.__class__.__name__.replace
                     ("Processor", " Processor")}: "
                  f"total {proc._total_procces} items processed, "
                  f"remaining {len(proc._storage)} on processor"
                  )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream..")
    print("== DataStream statistics ==")
    proc = DataStream()
    proc.print_processors_stats()
    print("Registering Numeric Processor")
    num_proc = NumericProcessor()
    proc.register_processor(num_proc)
    data_1 = ['Hello world', [3.14, -1, 2.71],
              [{'log_level': 'WARNING', 'log_message':
                'Telnet access! Use ssh instead'},
               {'log_level': 'INFO', 'log_message': 'User wil is connected'}],
              42,
              ['Hi', 'five']
              ]
    print(f"Send first batch of data on stream: {data_1}")
    proc.process_stream(data_1)
    print("== DataStream statistics ==")
    proc.print_processors_stats()
    print("Registering other data processors")
    print("Send the same batch again")
    tex_proc = TextProcessor()
    log_proc = LogProcessor()
    proc.register_processor(tex_proc)
    proc.register_processor(log_proc)
    print("== DataStream statistics ==")
    proc.process_stream(data_1)
    proc.print_processors_stats()
    print("Consume some elements from the data "
          "processors: Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num_proc.output()
    for _ in range(2):
        tex_proc.output()
    for _ in range(1):
        log_proc.output()

    print("== DataStream statistics ==")
    proc.print_processors_stats()


if __name__ == "__main__":
    main()
