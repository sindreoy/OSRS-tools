from pathlib import Path

from html_parser import scrape_quest_items
from quest_lists import get_pure_quest_list
from writers import write_aggregate_output, write_output_per_quest

# --- Run scraper ---

if __name__ == "__main__":
    pure_quests = get_pure_quest_list()
    quest_items = scrape_quest_items(pure_quests)

    per_quest_filename = Path(".out/quest_items_per_quest.txt")
    aggregate_filename = Path(".out/quest_items_aggregate.txt")
    if not (per_quest_filename.is_file()):
        write_output_per_quest(quest_items, per_quest_filename)
    if not (aggregate_filename.is_file()):
        write_aggregate_output(quest_items, aggregate_filename)
