from __future__ import annotations

import asyncio
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    """Find rooms slowly so voice-agent latency and failure recovery can be tested.

    Args:
        after_hour: Earliest acceptable hour, from 0 to 23.
        minimum_capacity: Minimum number of people the room must hold.

    The simulated service failure is returned as a structured tool result. This lets
    the agent explain the problem without receiving or repeating implementation
    details from a Python exception.
    """
    delay_seconds = float(os.getenv("ROOM_TOOL_DELAY_SECONDS", "5"))
    await asyncio.sleep(max(0, delay_seconds))
    if os.getenv("ROOM_TOOL_FAIL") == "1" or after_hour == 13:
        logger.error("Room availability could not be checked right now.")
        return {
            "status": "error",
            "message": "Room availability could not be checked right now.",
            "retryable": True,
        }
    return find_rooms(after_hour=after_hour, minimum_capacity=minimum_capacity)
