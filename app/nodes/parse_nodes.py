from typing import Dict, Any


def parse_and_normalize(state: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize the raw feed into a standard structure."""
    raw_feed = state.get("raw_feed", {})
    items = raw_feed.get("items", [])
    if not items:
        return state

    index = state.get("current_index", 0)
    if index >= len(items):
        return state

    item = items[index]
    normalized = {
        "title": item.get("title"),
        "description": item.get("description"),
        "source": item.get("source", raw_feed.get("source", "unknown")),
        "published_at": item.get("published_at"),
        "raw": item,
    }

    state.update(
        {
            "normalized_item": normalized,
            "title": normalized["title"],
            "source": normalized["source"],
            "published_at": normalized["published_at"],
        }
    )
    return state
