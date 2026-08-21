import asyncio

from adk_voice_workshop.room_tools import find_rooms, slow_find_rooms


def test_find_rooms_filters_time_and_capacity():
    result = find_rooms(after_hour=16, minimum_capacity=8)
    assert result["status"] == "success"
    assert [room["name"] for room in result["rooms"]] == ["Atlas", "Cedar"]


def test_find_rooms_rejects_invalid_hour():
    assert find_rooms(after_hour=24)["status"] == "error"


def test_slow_tool_can_fail(monkeypatch):
    monkeypatch.setenv("ROOM_TOOL_FAIL", "1")
    monkeypatch.setenv("ROOM_TOOL_DELAY_SECONDS", "0")

    async def run():
        result = await slow_find_rooms(15)
        assert result == {
            "status": "error",
            "message": "Room availability could not be checked right now.",
            "retryable": True,
        }

    asyncio.run(run())


def test_slow_tool_has_a_deliberate_delay(monkeypatch):
    monkeypatch.delenv("ROOM_TOOL_FAIL", raising=False)
    monkeypatch.setenv("ROOM_TOOL_DELAY_SECONDS", "5")

    async def run():
        try:
            await asyncio.wait_for(slow_find_rooms(15), timeout=0.01)
        except TimeoutError:
            return
        raise AssertionError("slow_find_rooms should not finish immediately")

    asyncio.run(run())
