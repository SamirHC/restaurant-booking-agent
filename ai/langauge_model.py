from abc import ABC, abstractmethod


class LanguageModel(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        pass
