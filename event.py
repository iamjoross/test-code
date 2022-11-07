import asyncio
from pyparsing import Any
import logging

subscribers: dict[str, Any] = dict()

def subscribe(event_type: str, fn):
    if not event_type in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(fn)

async def post_event(event_type: str, *args):
    try:
        if not event_type in subscribers:
            return
        for fn in subscribers[event_type]:
            return await fn(*args)
    except asyncio.CancelledError:
        logging.debug(f"[{event_type}] Propagated events cancelled.")
