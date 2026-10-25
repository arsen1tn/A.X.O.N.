from abc import ABC, abstractmethod

class BaseSkill(ABC):
    name = "base"

    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass

    @abstractmethod
    def run(self, text: str) -> str:
        pass