from axon.skills.base import BaseSkill

class HelloSkill(BaseSkill):
    name = "hello"

    def can_handle(self, text: str) -> bool:
        return text.lower().strip() == "ping"

    def run(self, text: str) -> str:
        return "pong"