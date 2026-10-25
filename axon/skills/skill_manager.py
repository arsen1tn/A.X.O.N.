from axon.core.logger import logger
from axon.skills.base import BaseSkill
import importlib
import inspect
import pkgutil
import axon.skills as skills_package

class SkillManager:
    def __init__(self):
        self.skills = []

    def register(self, skill: BaseSkill) -> None:
        self.skills.append(skill)
        logger.info(f"Registered skill: {skill.name}")

    def handle(self, text: str):
        for skill in self.skills:
            if skill.can_handle(text):
                logger.info(f"Skill used: {skill.name}")
                return skill.run(text)
        return None
    
    def load_skills(self) -> None:
        for module_info in pkgutil.iter_modules(skills_package.__path__):
            if module_info.name in ("base", "skill_manager"):
                continue

            module = importlib.import_module(f"axon.skills.{module_info.name}")

            for _, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, BaseSkill) and cls.__module__ == module.__name__ and cls is not BaseSkill:
                    self.register(cls())