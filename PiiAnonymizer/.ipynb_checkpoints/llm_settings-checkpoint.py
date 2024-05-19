
from typing import TypedDict, NotRequired

class LLMSettings(TypedDict):
    provider: str
    model: str
    temperature: NotRequired[float]
