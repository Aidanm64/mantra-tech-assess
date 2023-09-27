from typing import Callable
from tech_assess.domain import events, commands
from tech_assess.adapters.combiner import Combiner
from tech_assess.service.unit_of_work import UnitOfWork


def create_recording(cmd: commands.CreateRecording, uow: UnitOfWork):

    with uow:
        uow.recordings.create_new_recording(
            uuid=cmd.recording_uuid,
            audio_video_file=cmd.audio_video_file,
            audio_only_file=cmd.audio_only_file,
            video_only_file=cmd.video_only_file)


def combine_audio_video(event: events.RecordingCreated, uow: UnitOfWork,
                        combiner: Combiner):

    with uow:
        recording = uow.recordings.get_by_uuid(event.recording_uuid)

        combiner.train(video_file=recording.audio_video_filepath)

        combiner.combine(audio_filepath=recording.audio_only_filepath,
                         video_filepath=recording.video_only_filepath,
                         output_filepath=recording.combined_video_filepath)

        recording.update_combination_status(percentage=100)
        uow.recordings.update(recording)


def publish_recording_created(event: events.RecordingCreated,
                              publish: Callable):
    publish("recordings:created", event.dict())


def publish_combination_percentage_updated(
        event: events.RecordingCombinationPercentageUpdated,
        publish: Callable):
    publish("recordings:combination_percentage_updated", event.dict())


def publish_combination_completion(event: events.RecordingCombinationCompleted,
                                   publish: Callable):
    publish("recordings:combination_completed", event.dict())


COMMAND_HANDLERS = {commands.CreateRecording: create_recording}

EVENT_HANDLERS = {
    events.RecordingCreated: [combine_audio_video, publish_recording_created],
    events.RecordingCombinationPercentageUpdated:
    [publish_combination_percentage_updated],
    events.RecordingCombinationCompleted: [publish_combination_completion]
}