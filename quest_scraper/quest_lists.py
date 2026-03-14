from pathlib import Path

from quest_scraper.custom_types import QuestSection
from quest_scraper.markdown_parser import load_quests_with_breaks


def get_pure_quest_list() -> list[QuestSection]:
    # Replace with your full quest list (use exact wiki page titles)
    return load_quests_with_breaks(Path("quest_scraper/QuestOrderForPures.md"))
