import sys
from pathlib import Path

from quest_scraper.html_parser import scrape_quest_items
from quest_scraper.quest_lists import get_pure_quest_list
from quest_scraper.writers import write_aggregate_output, write_output_per_quest

# --- Run scraper ---

if __name__ == "__main__":
    pure_quests = get_pure_quest_list()
    quest_name_chunks = [
        [quests for quests in chunk["quests"]] for chunk in pure_quests
    ]
    per_quest_filename = Path(".out/quest_items_per_quest.txt")
    aggregate_filename = Path(".out/quest_items_aggregate.txt")
    if per_quest_filename.is_file() or aggregate_filename.is_file():
        shouldOverwrite = (
            input(
                "The output files already exist. Do you want to overwrite them? (y/n): "
            )
            .strip()
            .lower()
        )
        if shouldOverwrite != "y":
            sys.exit(
                f"Output file {per_quest_filename} or {aggregate_filename} already exists. Please remove it before running the scraper."
            )
    quest_items = scrape_quest_items(pure_quests)
    write_output_per_quest(quest_items, per_quest_filename)
    write_aggregate_output(quest_items, aggregate_filename)
