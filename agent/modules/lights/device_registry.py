import logging
import httpx
from .config import KASA_EMAIL, KASA_PASSWORD, KASA_CLOUD_URL, TERMINAL_UUID, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

_token: str = ""
_devices: dict[str, dict] = {}


async def _login() -> str:
    payload = {
        "method": "login",
        "params": {
            "appType": "Kasa_Android",
            "appVersion": "3.4.507",
            "cloudUserName": KASA_EMAIL,
            "cloudPassword": KASA_PASSWORD,
            "terminalUUID": TERMINAL_UUID,
        },
    }
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.post(KASA_CLOUD_URL, json=payload)
        response.raise_for_status()
        data = response.json()

    token = data.get("result", {}).get("token", "")
    if not token:
        raise RuntimeError(f"Login failed: {data.get('msg', 'unknown error')}")
    return token


async def _fetch_devices(token: str) -> dict[str, dict]:
    payload = {"method": "getDeviceList", "params": {}}
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.post(f"{KASA_CLOUD_URL}?token={token}", json=payload)
        response.raise_for_status()
        data = response.json()

    devices = {}
    for d in data.get("result", {}).get("deviceList", []):
        name = d.get("alias", "").lower().strip()
        devices[name] = {
            "device_id": d.get("deviceId"),
            "device_type": d.get("deviceType", ""),
            "model": d.get("deviceModel", ""),
        }
        logger.info("Found device: %s (%s)", name, d.get("deviceModel"))
    return devices


async def load() -> None:
    global _token, _devices
    try:
        _token = await _login()
        _devices = await _fetch_devices(_token)
        logger.info("Loaded %d Kasa devices.", len(_devices))
    except Exception as e:
        logger.error("Failed to load Kasa devices: %s", e)


def get_token() -> str:
    return _token


def get_device(name: str) -> dict | None:
    return _devices.get(name.lower().strip())
