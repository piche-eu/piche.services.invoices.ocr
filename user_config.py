from dataclasses import dataclass


@dataclass
class UserConfig:
    llm: str = "MISTAL"
    AUTH_KEY: str = ""
    return_metrics: bool = True
    validate: bool = True
    temperature: float = 0.7
    top_k: int = 3
    length_penalty: float = (
        1.2  # (? adjust the value, the llm response schould contain the same amount of tokens as produced by OCR )
    )


@dataclass
class Metric:
    semantic_entropy: str
    uncertainty: str
    groundess: str
