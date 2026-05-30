from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class WebSearchInput(BaseModel):
    query: str = Field(..., description="The search query.")


class OpenBrowserInput(BaseModel):
    url: str = Field(..., description="The URL to open.")


class PlayYoutubeInput(BaseModel):
    query: str = Field(..., description="The YouTube search query.")


class SetReminderInput(BaseModel):
    text: str = Field(..., description="Reminder text.")
    datetime_iso: str = Field(..., description="ISO 8601 datetime string.")


class LightAction(str, Enum):
    on = "on"
    off = "off"
    brightness = "brightness"


class ControlLightInput(BaseModel):
    device_name: str = Field(..., description="Name of the light device.")
    action: LightAction
    value: Optional[int] = Field(None, ge=0, le=100, description="Brightness 0-100.")
