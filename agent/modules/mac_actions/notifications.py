import logging
import subprocess

logger = logging.getLogger(__name__)


def notify(title: str, message: str) -> str:
    script = f'display notification "{message}" with title "{title}"'
    try:
        subprocess.run(["osascript", "-e", script], check=True, timeout=10)
        return f"Notification sent: '{title} — {message}'."
    except subprocess.TimeoutExpired:
        logger.error("osascript timed out sending notification")
        return "Failed to send notification: timed out."
    except subprocess.CalledProcessError as e:
        logger.error("osascript error sending notification: %s", e)
        return f"Failed to send notification: {e}"
