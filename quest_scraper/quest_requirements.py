import time
from collections import defaultdict
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://oldschool.runescape.wiki/w/"
HEADERS = {"User-Agent": "OSRS-Quest-Item-Scraper/1.0"}
REQUEST_DELAY = 0.8  # seconds between requests

# Replace with your full quest list (use exact wiki page titles)
CHUNK_ONE = [
    "Rune Mysteries",
    "The Restless Ghost",
    "Imp catcher",
    "Witch's potion",
    "Doric's quest",
    "Goblin Diplomacy",
    "Witch's house",
    "Druidic Ritual",
    "Death plateau",
    "The knight's sword",
    "Gertrude's cat",
    "Vampyre slayer",
    "Ernest the chicken",
    "The Tourist Trap",
    "Dwarf Cannon",
    "Waterfall Quest",
    "Monk's Friend",
    "Fight Arena",
    "Tree Gnome Village",
]

# 30 Firemaking
CHUNK_TWO = [
    "Sea slug",
    "Plague city",
    "Biohazard",
    "Fishing contest",
    "Demon slayer",
    "Cook's assistant",
    "Recipe for Disaster/Another Cook's Quest",
    "Recipe for Disaster/Freeing the Goblin generals",
    "Recipe for Disaster/Freeing the Mountain Dwarf",
    "Murder Mystery",
    "Hazeel Cult",
    "X Marks the Spot",
    "Client of Kourend",
    "The Queen of Thieves",
    "Tribal Totem",
    "The Lost Tribe",
    "Death to the Dorgeshuun",
    "Children of the Sun",
    "Shield of Arrav",
    "Ethically Acquired Antiquities",
    "The Feud",
    "Death on the Isle",
    "Jungle Potion",
]

# 10 herblore
CHUNK_THREE = [
    "The Dig Site",
    "Mountain Daughter",
    "The Giant Dwarf",
    "Priest in Peril",
    "Ghosts Ahoy",
    "Making History",
    "Horror from the Deep",
    "Elemental Workshop I",
    "The golem",
    "Elemental Workshop II",  # optional, start while at Dig Site in The Golem quest,
    "Sleeping Giants",  # optional
    "Shades of Mort'ton",  # optional
    "Shadow of the storm",
    "Recipe for Disaster/Freeing Evil Dave",
]

# 30 cooking
CHUNK_FOUR = [
    "Big Chompy Bird Hunting",
    "Tai Bwo Wannai Trio",
    "Recipe for Disaster/Freeing Pirate Pete",
]

# 41 cooking
CHUNK_FIVE = [
    "Recipe for Disaster/Freeing Skrach Uglogwee",
    "Another Slice of H.A.M",  # optional
]

# 40 mining
CHUNK_SIX = [
    "Watchtower",  # optional
    "Icthlarin's Little Helper",  # optional
    "Contact!",  # optional, also hard without prayer
    "Twilight's Promise",
    "A Porcine of Interest",
]

# 35 woodcutting
CHUNK_SEVEN = [
    "Animal Magnetism",
    "Lost City",
    "The Forsaken Tower",  # optional
    "Troll Stronghold",
]

# 31 herblore
CHUNK_NINE = [
    "Eadgar's Ruse",
    "Troll Romance",
    "Haunted Mine",
    "Underground Pass (optional, gives attack xp)",
]

# 26 construction
CHUNK_TEN = [
    "Getting Ahead",  # optional
    "Shilo Village",  # optional
    "Family Crest",  # optional
    "Scorpion Catcher",
    "Desert Treasure",
    "Curse of the Empty Lord",
]

# 60 magic
CHUNK_ELEVEN = ["Mage Arena I"]

QUESTS = (
    CHUNK_ONE
    + CHUNK_TWO
    + CHUNK_THREE
    + CHUNK_FOUR
    + CHUNK_FIVE
    + CHUNK_SIX
    + CHUNK_SEVEN
    + CHUNK_NINE
    + CHUNK_TEN
    + CHUNK_ELEVEN
)
# --- Helpers ---


def quest_url(quest_name: str) -> str:
    slug = quest_name.replace(" ", "_")
    return BASE_URL + quote_plus(slug, safe="_")


def get_soup(url: str, timeout: int = 15):
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


# --- Core scraping logic ---


def parse_li_item(li) -> tuple[int, str] | None:
    """
    Extracts (quantity, item_name) from an <li> element.
    Example:
        <li>4 <a href="/w/Copper_ore" title="Copper ore">copper ores</a></li>
    Returns:
        (4, "Copper ore")
    If no number is present, quantity defaults to 1.
    """

    # Find the anchor with the item title
    a = li.find("a", title=True)
    if not a:
        return None  # skip malformed entries

    item_name = a["title"].strip()

    # Extract leading number (if any)
    text = li.get_text(" ", strip=True)
    parts = text.split()

    quantity = 1
    if parts and parts[0].isdigit():
        quantity = int(parts[0])

    return (quantity, item_name)


def extract_required_items(soup: BeautifulSoup) -> list[tuple[int, str]]:
    """
    Extracts required items as (quantity, item_name) tuples.
    Looks for:
      <th class="questdetails-header">Items required</th>
    Then extracts the corresponding:
      <td class="questdetails-info"> ... </td>
    """

    tables = soup.find_all("table", class_="questdetails")
    if not tables:
        return []

    for table in tables:
        rows = table.find_all("tr")
        for i, row in enumerate(rows):

            # ✔ Corrected: questdetails-header is in <th>, not <td>
            header = row.find("th", class_="questdetails-header")
            if not header:
                continue

            if header.get_text(strip=True).lower() == "items required":

                # The info cell is usually in the same row
                info_cell = row.find("td", class_="questdetails-info")

                # But sometimes it's in the next row
                if not info_cell and i + 1 < len(rows):
                    info_cell = rows[i + 1].find("td", class_="questdetails-info")

                if not info_cell:
                    return []

                items = []

                # Case 1: structured <li> list
                for li in info_cell.find_all("li"):
                    # Skip nested <li> elements (only accept direct children of the info cell)
                    if li.find_parent("li"):
                        continue

                    parsed = parse_li_item(li)
                    if parsed:
                        items.append(parsed)

                # Case 2: fallback — plain text
                if not items:
                    raw = info_cell.get_text(" ", strip=True)
                    if raw and raw.lower() != "none":
                        items.append((1, raw))

                return items

    return []


def scrape_quest_items(quests: list[str]) -> dict[str, list[tuple[int, str]]]:
    results = {}
    failed_quests = []

    for quest in quests:
        url = quest_url(quest)
        print(f"Scraping: {quest} → {url}")

        try:
            soup = get_soup(url)
            items = extract_required_items(soup)
            results[quest] = items
        except Exception as e:
            print(f"Error scraping {quest}: {e}")
            results[quest] = []
            failed_quests.append(quest)

        time.sleep(REQUEST_DELAY)

    if failed_quests:
        print("\n\nFailed to obtain information for the following quests:")
        for failed in failed_quests:
            print(f"  - {failed}")
    return results


def aggregate_items(quest_items: dict[str, list[tuple[int, str]]]) -> dict[str, int]:
    """
    Takes:
        {
            "Quest A": [(4, "Copper ore"), (1, "Bucket")],
            "Quest B": [(2, "Copper ore")],
            ...
        }

    Returns:
        {
            "Copper ore": 6,
            "Bucket": 1,
            ...
        }
    """

    totals = defaultdict(int)

    for quest, items in quest_items.items():
        for qty, name in items:
            # Normalize item names (wiki titles are already consistent)
            clean_name = name.strip()

            # Add quantity
            totals[clean_name] += qty

    return dict(totals)


# --- Run scraper ---

if __name__ == "__main__":
    quest_items = scrape_quest_items(QUESTS)

    print("\n=== Required Items by Quest ===")
    for quest, items in quest_items.items():
        print(f"\n{quest}:")
        if items:
            for item in items:
                print(f"  - {item}")
        else:
            print("  (No items found)")

    total_list = aggregate_items(quest_items)
    print("\n\n=== Total List of Required Items ===")
    for item, qty in total_list.items():
        print(f"{item}: {qty}")
