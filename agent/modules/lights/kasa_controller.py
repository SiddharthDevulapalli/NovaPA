import json
import logging
import httpx
from .config import KASA_CLOUD_URL, REQUEST_TIMEOUT
from .device_registry import get_token, get_device

logger = logging.getLogger(__name__)


def _build_command(action: str, value: int | None) -> str:
    if action == "on":
        cmd = {"smartlife.iot.smartbulb.lightingservice": {"transition_light_state": {"on_off": 1}}}
    elif action == "off":
        cmd = {"smartlife.iot.smartbulb.lightingservice": {"transition_light_state": {"on_off": 0}}}
    elif action == "brightness" and value is not None:
        cmd = {"smartlife.iot.smartbulb.lightingservice": {"transition_light_state": {"brightness": value, "on_off": 1}}}
    else:
        return ""
    return json.dumps(cmd)


async def control(device_name: str, action: str, value: int | None = None) -> str:
    device = get_device(device_name)
    if device is None:
        return f"Device '{device_name}' not found. Available devices can be checked in the Kasa app."

    command = _build_command(action, value)
    if not command:
        return f"Unknown action: {action}"

    token = get_token()
    payload = {
        "method": "passthrough",
        "params": {
            "deviceId": device["device_id"],
            "requestData": command,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(f"{KASA_CLOUD_URL}?token={token}", json=payload)
            response.raise_for_status()
            data = response.json()

        if data.get("error_code", -1) != 0:
            return f"Light command failed: {data.get('msg', 'unknown error')}"

        suffix = f" to {value}%" if action == "brightness" else ""
        return f"Light '{device_name}' turned {action}{suffix}."

    except httpx.TimeoutException:
        logger.error("Kasa cloud request timed out.")
        return "Light command timed out."
    except Exception as e:
        logger.error("Kasa cloud error: %s", e)
        return f"Light command failed: {e}"
