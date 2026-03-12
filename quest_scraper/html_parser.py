import time

from bs4 import BeautifulSoup
from utils import get_soup, quest_url

REQUEST_DELAY = 0.3  # seconds between requests


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
