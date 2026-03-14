from collections import defaultdict
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "OSRS-Quest-Item-Scraper/1.0"}
BASE_URL = "https://oldschool.runescape.wiki/w/"


def quest_url(quest_name: str) -> str:
    slug = quest_name.replace(" ", "_")
    return BASE_URL + quote_plus(slug, safe="_")


def get_soup(url: str, timeout: int = 15):
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


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

    totals: dict[str, int] = defaultdict(int)

    for _, items in quest_items.items():
        for qty, name in items:
            # Normalize item names (wiki titles are already consistent)
            clean_name = name.strip()

            # Add quantity
            totals[clean_name] += qty

    return dict(totals)
