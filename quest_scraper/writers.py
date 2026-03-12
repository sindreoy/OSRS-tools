from pathlib import Path

from utils import aggregate_items


def write_output_per_quest(
    quest_items: dict[str, list[tuple[int, str]]],
    file_path: Path = Path(".out/quest_items_per_quest.txt"),
):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        for quest, items in quest_items.items():
            f.write(f"{quest}:\n")
            if items:
                for qty, name in items:
                    f.write(f"  - {qty} x {name}\n")
            else:
                f.write("  (No items found)\n")
            f.write("\n")


def write_aggregate_output(
    quest_items: dict[str, list[tuple[int, str]]],
    file_path: Path = Path(".out/quest_items_aggregate.txt"),
):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    totals = aggregate_items(quest_items)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=== Total List of Required Items ===\n")
        for item, qty in totals.items():
            f.write(f"{item}: {qty}\n")
