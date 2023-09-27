
from tech_assess.service.unit_of_work import UnitOfWork


def get_recording(uow: UnitOfWork, recording_uuid: str):
    recording = uow.recordings.get_by_uuid(uuid=recording_uuid)
    return recording.to_dict()


def get_recording_output(uow: UnitOfWork, recording_uuid: str):
    recording = uow.recordings.get_by_uuid(uuid=recording_uuid)
    return recording.audio_video_filepath
