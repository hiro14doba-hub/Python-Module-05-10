from abc import ABC, abstractmethod
from typing import Any, Union


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0

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

    def ingest(self, data: Union[int, float, list[Union[int, float]]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(str(item))
        else:
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
                self._storage.append(item)
        else:
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
                msg = f"{item['log_level']}: {item['log_message']}"
                self._storage.append(msg)
        else:
            msg = f"{data['log_level']}: {data['log_message']}"
            self._storage.append(msg)


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    print("Testing Numeric Processor...")
    num_proc = NumericProcessor()
    print(f"Trying to validate input'42': {num_proc.validate(42)}")
    print(f"Trying to validate input'Hello': {num_proc.validate("Hello")}")
    print("Test invalid ingestion of string'foo' without prior validation:")
    try:
        num_proc.ingest("foo")  # type: ignore[arg-type]
    except Exception as e:
        print(f"Got exception: {e}")
    num_data = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_data}")
    num_proc.ingest(num_data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num_proc.output()
        print(f"Numeric value {rank}: {val}")

    print("Testing Text Processor...")
    tex_proc = TextProcessor()
    print(f"Trying to validate input'42': {tex_proc.validate(42)}")
    tex_data = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {tex_data}")
    tex_proc.ingest(tex_data)
    print("Extracting 1 value...")
    rank, val = tex_proc.output()
    print(f"Text value {rank}: {val}")

    print("Testing Log Processor...")
    log_proc = LogProcessor()
    print(f"Trying to validate input'Hello': {log_proc.validate("Hallo")}")
    log_data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {log_data}")
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {rank}: {val}")


if __name__ == "__main__":
    main()
