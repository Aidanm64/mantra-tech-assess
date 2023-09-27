from tech_assess.domain.events import Event
from tech_assess.domain import events

from typing import List
from pydantic import BaseModel


class Entity(BaseModel):
    uuid: str
    events: List[Event] = []

    def __hash__(self):
        return hash(self.uuid)

    @classmethod
    def from_dict(cls, obj):
        if obj.get('uuid', None) is None:
            obj['uuid'] = str(uuid4())
        entity = cls.parse_obj(obj)
        return entity


class Recording(Entity):
    audio_video_filepath: str
    audio_only_filepath: str
    video_only_filepath: str
    combined_video_filepath: str
    combination_percentage: int = 0

    def to_dict(self):
        return self.dict()

    def update_combination_completion_percentage(self, percent):
        self.combination_percentage = percent
        self.events.append(
            events.RecordingCombinationPercentageUpdated(
                recording_uuid=self.uuid, completion_percentage=percent))
        if self.combination_completed:
            self.events.append(
                events.RecordingCombinationCompleted(recording_uuid=self.uuid))

    @property
    def combination_completed(self):
        return self.combination_percentage == 100

