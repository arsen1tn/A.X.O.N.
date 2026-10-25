from datetime import datetime
from axon.skills.base import BaseSkill

class TimeSkill(BaseSkill):
    name = "time"

    def can_handle(self, text: str) -> bool:
        message = text.lower().strip()

        exact = ["time", "the time", "clock"]
        if message in exact:
            return True

        strong = ["time is it", "current time", "time now"]
        if any(p in message for p in strong):
            return True

        weak = ["what time"]
        return len(message.split()) <= 6 and any(p in message for p in weak)
    
    def run(self, text: str) -> str:
        return "It is " + datetime.now().strftime("%H:%M")