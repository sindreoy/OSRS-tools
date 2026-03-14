from typing import List, Tuple, TypedDict


class SkillRequirement(TypedDict):
    level: int
    skill: str


class QuestSection(TypedDict):
    requirements: List[SkillRequirement]
    quests: List[str]


RequiredItem = Tuple[int, str]  # (quantity, item_name)
