TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for current information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query."}
            },
            "required": ["query"],
        },
    },
    {
        "name": "open_browser",
        "description": "Open a URL in the user's browser.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to open."}
            },
            "required": ["url"],
        },
    },
    {
        "name": "play_youtube",
        "description": "Search YouTube and play the top result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The YouTube search query."}
            },
            "required": ["query"],
        },
    },
    {
        "name": "set_reminder",
        "description": "Set a reminder on the user's Mac.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Reminder text."},
                "datetime_iso": {"type": "string", "description": "ISO 8601 datetime string."},
            },
            "required": ["text", "datetime_iso"],
        },
    },
    {
        "name": "control_light",
        "description": "Control a Kasa smart light.",
        "input_schema": {
            "type": "object",
            "properties": {
                "device_name": {"type": "string", "description": "Name of the light device."},
                "action": {"type": "string", "enum": ["on", "off", "brightness"], "description": "Action to perform."},
                "value": {"type": "integer", "description": "Brightness 0-100. Only required for brightness action."},
            },
            "required": ["device_name", "action"],
        },
    },
]
