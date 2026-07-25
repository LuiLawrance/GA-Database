from pathlib import Path
from util_file import new_json

import json

_BASE = Path(__file__).parent.parent / "GA-Library" / "DATA_GA" / "PRICING_GA"

LOCAL_LISTINGS = new_json("DATA_GA/PRICING_GA/LOCAL_LISTINGS.json")
LOCAL_SALES = new_json("DATA_GA/PRICING_GA/LOCAL_SALES.json")
LOCAL_IDS = new_json("DATA_GA/PRICING_GA/LOCAL_ID_TCGPLAYER.json")

TARGET_LISTINGS = _BASE / "LISTINGS.json"
TARGET_SALES = _BASE / "SALES.json"
TARGET_IDS = _BASE / "ID_TCGPLAYER.json"


def _sync(target: Path, local: Path) -> None:
    with target.open("r", encoding="utf-8") as f:
        target_data = json.load(f)

    with local.open("r", encoding="utf-8") as f:
        local_data = json.load(f)

    for card_id, editions in target_data.items():
        for edition_id, foils in editions.items():
            filled = {foil_id: entries for foil_id, entries in foils.items() if entries}

            if not filled:
                continue

            if card_id not in local_data:
                local_data[card_id] = {}

            if edition_id not in local_data[card_id]:
                local_data[card_id][edition_id] = {}

            for foil_id, entries in filled.items():
                if foil_id not in local_data[card_id][edition_id]:
                    local_data[card_id][edition_id][foil_id] = entries

    with local.open("w", encoding="utf-8") as f:
        json.dump(local_data, f, indent=4, ensure_ascii=False)


# Duplicate the card_id -> product_id mapping, dropping the last_sales/last_listings fields.
def _sync_ids(target: Path, local: Path) -> None:
    with target.open("r", encoding="utf-8") as f:
        target_data = json.load(f)

    local_data = {card_id: {"product_id": info["product_id"]} for card_id, info in target_data.items()}

    with local.open("w", encoding="utf-8") as f:
        json.dump(local_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    _sync(TARGET_LISTINGS, LOCAL_LISTINGS)
    _sync(TARGET_SALES, LOCAL_SALES)
    _sync_ids(TARGET_IDS, LOCAL_IDS)
