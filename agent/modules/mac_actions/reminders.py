import logging
import subprocess
from datetime import datetime

logger = logging.getLogger(__name__)


def set_reminder(text: str, dt: datetime) -> str:
    date_str = dt.strftime("%B %d, %Y %H:%M:%S")
    script = f'''
    tell application "Reminders"
        set myList to first list
        make new reminder at end of myList with properties {{name:"{text}", due date:date "{date_str}"}}
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True, timeout=10)
        return f"Reminder set: '{text}' at {date_str}."
    except subprocess.TimeoutExpired:
        logger.error("osascript timed out setting reminder")
        return "Failed to set reminder: timed out."
    except subprocess.CalledProcessError as e:
        logger.error("osascript error setting reminder: %s", e)
        return f"Failed to set reminder: {e}"
