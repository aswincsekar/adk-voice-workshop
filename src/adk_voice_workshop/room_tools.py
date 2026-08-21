from __future__ import annotations

import asyncio
import os

ROOMS = [
    {"name": "Orchid", "available_from": 15, "capacity": 4},
    {"name": "Atlas", "available_from": 16, "capacity": 8},
    {"name": "Cedar", "available_from": 17, "capacity": 12},
]


def find_rooms(after_hour: int, minimum_capacity: int = 1) -> dict:
    """Find rooms available at or after an hour using a 24-hour clock.

    Args:
        after_hour: Earliest acceptable hour, from 0 to 23.
        minimum_capacity: Minimum number of people the room must hold.
    """
    if not 0 <= after_hour <= 23:
        return {"status": "error", "message": "after_hour must be between 0 and 23"}
    if minimum_capacity < 1:
        return {"status": "error", "message": "minimum_capacity must be positive"}

    matches = [
        room
        for room in ROOMS
        if room["available_from"] >= after_hour and room["capacity"] >= minimum_capacity
    ]
    return {"status": "success", "rooms": matches}


async def slow_find_rooms(after_hour: int, minimum_capacity: int = 1) -> dict:
    """Find rooms slowly so voice-agent latency and failure recovery can be tested."""
    await asyncio.sleep(5)
    if os.getenv("ROOM_TOOL_FAIL") == "1" or after_hour == 13:
        raise RuntimeError("The room service is temporarily unavailable")
    return find_rooms(after_hour=after_hour, minimum_capacity=minimum_capacity)

