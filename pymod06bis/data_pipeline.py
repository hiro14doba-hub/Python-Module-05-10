from abc import ABC, abstractmethod
from typing import Any, Union, Sequence, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0
        self._total_process: int = 0

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
                self._total_process += 1
                self._storage.append(str(item))
        else:
            self._total_process += 1
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
                self._total_process += 1
                self._storage.append(item)
        else:
            self._total_process += 1
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
                self._total_process += 1
                msg = f"{item['log_level']}: {item['log_message']}"
                self._storage.append(msg)
        else:
            self._total_process += 1
            msg = f"{data['log_level']}: {data['log_message']}"
            self._storage.append(msg)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []
        self._total_process: int = 0

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            handled = False
            for proc in self.processors:
                if proc.validate(item):
                    proc.ingest(item)
                    self._total_process += 1
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{item}"
                )

    def print_processors_stats(self) -> None:
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            proc_name = proc.__class__.__name__.replace(
                "Processor", " Processor")
            print(
                f"{proc_name}: total {proc._total_process} items processed, "
                f"remaining {len(proc._storage)} on processor"
            )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            extracted: list[tuple[int, str]] = []
            for _ in range(nb):
                try:
                    item = proc.output()
                    extracted.append(item)
                except IndexError:
                    break
            if extracted:
                plugin.process_output(extracted)


class CsvPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        print("CSV Output:")
        csv_list: list[str] = []
        for _, value in data:
            csv_list.append(value)
        print(",".join(csv_list))


class JsonPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        Json_dict = [f'"item_{rank}": "{value}"' for rank, value in data]
        print("JSON Output:")
        print("{" + ",".join(Json_dict) + "}")


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    proc = DataStream()
    print("== DataStream statistics ==")
    proc.print_processors_stats()
    print("Registering Processors")
    data_1 = ['Hello world', [3.14, -1, 2.71],
              [{'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead'},
               {'log_level': 'INFO', 'log_message': 'User wil is connected'}],
              42, ['Hi', 'five']]
    print(f"Send first batch of data on stream: {data_1}")
    print("== DataStream statistics ==")
    num_proc = NumericProcessor()
    tex_proc = TextProcessor()
    log_proc = LogProcessor()
    proc.register_processor(num_proc)
    proc.register_processor(tex_proc)
    proc.register_processor(log_proc)
    proc.process_stream(data_1)
    proc.print_processors_stats()
    print("Send 3 processed data from each processor to a CSV plugin:")
    proc.output_pipeline(3, CsvPlugin())
    print("== DataStream statistics ==")
    proc.print_processors_stats()
    data_2 = [21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
              [{'log_level': 'ERROR', 'log_message': '500 server crash'},
              {'log_level': 'NOTICE', 'log_message':
               'Certificate expires in 10 days'}],
              [32, 42, 64, 84, 128, 168], 'World hello']
    print(f"Send another batch of data: {data_2}")
    print("== DataStream statistics ==")
    proc.process_stream(data_2)
    proc.print_processors_stats()
    print("Send 5 processed data from each processor to a JSON plugin:")
    proc.output_pipeline(5, JsonPlugin())
    print("== DataStream statistics ==")
    proc.print_processors_stats()


if __name__ == "__main__":
    main()
