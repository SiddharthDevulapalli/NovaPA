import json
import logging
from datetime import datetime
from pydantic import ValidationError

from .tool_models import (
    WebSearchInput,
    OpenBrowserInput,
    PlayYoutubeInput,
    SetReminderInput,
    ControlLightInput,
)
from server.modules.web_search.searcher import search
from agent.modules.browser.opener import open_url
from agent.modules.browser.youtube import play_youtube
from agent.modules.mac_actions.reminders import set_reminder
from agent.modules.lights.kasa_controller import control as kasa_control

logger = logging.getLogger(__name__)

_SCHEMAS = {
    "web_search": WebSearchInput,
    "open_browser": OpenBrowserInput,
    "play_youtube": PlayYoutubeInput,
    "set_reminder": SetReminderInput,
    "control_light": ControlLightInput,
}


async def dispatch(tool_name: str, tool_args: dict) -> str:
    schema = _SCHEMAS.get(tool_name)
    if schema is None:
        return f"Unknown tool: {tool_name}"
    try:
        validated = schema(**tool_args)
    except ValidationError as e:
        return f"Invalid args for {tool_name}: {e.errors()}"

    handlers = {
        "web_search": _web_search,
        "open_browser": _open_browser,
        "play_youtube": _play_youtube,
        "set_reminder": _set_reminder,
        "control_light": _control_light,
    }
    return await handlers[tool_name](validated)


async def _web_search(args: WebSearchInput) -> str:
    logger.info("web_search: query=%s", args.query)
    results = await search(args.query)
    if not results:
        return "No results found."
    return json.dumps(results)


async def _open_browser(args: OpenBrowserInput) -> str:
    logger.info("open_browser: url=%s", args.url)
    return open_url(args.url)


async def _play_youtube(args: PlayYoutubeInput) -> str:
    logger.info("play_youtube: query=%s", args.query)
    return play_youtube(args.query)


async def _set_reminder(args: SetReminderInput) -> str:
    logger.info("set_reminder: %s at %s", args.text, args.datetime_iso)
    dt = datetime.fromisoformat(args.datetime_iso)
    return set_reminder(args.text, dt)


async def _control_light(args: ControlLightInput) -> str:
    logger.info("control_light: %s %s %s", args.device_name, args.action, args.value)
    return await kasa_control(args.device_name, args.action.value, args.value)
