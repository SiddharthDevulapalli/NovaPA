import logging
import subprocess
from datetime import datetime

logger = logging.getLogger(__name__)


def set_alarm(dt: datetime) -> str:
    date_str = dt.strftime("%B %d, %Y %H:%M:%S")
    script = f'''
    tell application "Reminders"
        set myList to first list
        make new reminder at end of myList with properties {{name:"Alarm", due date:date "{date_str}"}}
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True, timeout=10)
        return f"Alarm set for {date_str}."
    except subprocess.TimeoutExpired:
        logger.error("osascript timed out setting alarm")
        return "Failed to set alarm: timed out."
    except subprocess.CalledProcessError as e:
        logger.error("osascript error setting alarm: %s", e)
        return f"Failed to set alarm: {e}"
