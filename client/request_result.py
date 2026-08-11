from dataclasses import dataclass

@dataclass
class RequestResult:
    response: object
    elapsed_time: float