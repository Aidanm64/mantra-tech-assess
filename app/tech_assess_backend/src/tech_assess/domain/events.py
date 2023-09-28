
from pydantic import BaseModel


class Event(BaseModel):
    pass


class RecordingEvent(Event):
    recording_uuid: str


class RecordingCreated(RecordingEvent):
    pass


class RecordingCombinationPercentageUpdated(RecordingEvent):
    completion_percentage: int


class RecordingCombinationCompleted(RecordingEvent):
    pass


