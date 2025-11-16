from typing import Dict, Any
import json
import httpx


async def fetch_threat_feed(state: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch threat feed from HTTP or local sample file."""
    feed_url = state.get("feed_url")
    if feed_url and feed_url.startswith("http"):
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(feed_url)
            resp.raise_for_status()
            raw_feed = resp.json()
    else:
        sample_path = state.get("sample_path", "app/sample_data/sample_feed.json")
        with open(sample_path, "r", encoding="utf-8") as f:
            raw_feed = json.load(f)

    return {**state, "raw_feed": raw_feed}
