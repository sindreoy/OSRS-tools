import re
from pathlib import Path

from quest_scraper.custom_types import QuestSection, SkillRequirement


def load_quests_with_breaks(
    path: Path,
) -> list[QuestSection]:
    text = Path(path).read_text(encoding="utf-8")

    sections = []
    current_section: QuestSection = {
        "requirements": [],
        "quests": [],
    }

    # Matches: "## 30 Firemaking, 40 Crafting"
    header_pattern = re.compile(r"^##\s+(.*)$")

    # Matches individual requirements inside the header
    req_pattern = re.compile(r"(\d+)\s+([A-Za-z ]+)")

    # Matches quest lines: "- Quest Name (notes)"
    quest_pattern = re.compile(r"^\s*-\s+(.*)$")

    # Removes parentheses and their contents
    paren_pattern = re.compile(r"\s*\(.*?\)\s*")

    for line in text.splitlines():
        line = line.rstrip()

        # Detect skill requirement header
        header_match = header_pattern.match(line)
        if header_match:
            # Save previous section if it contains data
            if current_section["requirements"] or current_section["quests"]:
                sections.append(current_section)

            req_text = header_match.group(1)
            requirements: list[SkillRequirement] = []

            for level, skill in req_pattern.findall(req_text):
                requirements.append({"level": int(level), "skill": skill.strip()})

            current_section = {"requirements": requirements, "quests": []}
            continue

        # Detect quest lines
        quest_match = quest_pattern.match(line)
        if quest_match:
            raw = quest_match.group(1).strip()

            # Remove parentheses and their contents
            cleaned = paren_pattern.sub("", raw).strip()

            current_section["quests"].append(cleaned)

    # Append last section
    if current_section["requirements"] or current_section["quests"]:
        sections.append(current_section)

    return sections
