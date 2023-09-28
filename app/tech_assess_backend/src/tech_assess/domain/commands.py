from uuid import uuid4

from pydantic import BaseModel
from werkzeug.datastructures import FileStorage


class Command(BaseModel):

    class Config:
        arbitrary_types_allowed = True


class CreateRecording(Command):
    recording_uuid: str
    audio_video_file: FileStorage
    audio_only_file: FileStorage
    video_only_file: FileStorage

    @staticmethod
    def from_dict(obj):
        return CreateRecording(recording_uuid=obj.get('recording_uuid', str(uuid4())),
                           audio_video_file=obj['audio_video_file'],
                           audio_only_file=obj['audio_only_file'],
                           video_only_file=obj['video_only_file'])
