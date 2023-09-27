from tech_assess.domain.model import Entity, Recording
from tech_assess.domain import events
from tech_assess.adapters import mongodb
from tech_assess.config import get_file_storage_config
import os


class Repository:

    def __init__(self):
        self.seen = set()

    def add(self, entity: Entity):
        self._add(entity)
        self.seen.add(entity)

    def get(self, id: str) -> Entity:
        entity = self._get(id)
        if entity:
            self.seen.add(entity)
        return entity

    def get_by_uuid(self, uuid: str) -> Entity:
        entity = self._get_by_uuid(uuid)
        if entity:
            self.seen.add(entity)

        return entity

    def update(self, entity: Entity):
        self._update(entity)
        self.seen.add(entity)

    def _add(self, entity):
        raise NotImplementedError

    def _update(self, entity):
        raise NotImplementedError

    def _get(self, id):
        raise NotImplementedError

    def _get_by_uuid(self, uuid):
        raise NotImplementedError


class MongoRepository(Repository):

    def __init__(self, entity_class, mongo_collection):
        super().__init__()
        self.collection = mongo_collection
        self.entity_class = entity_class

    def _add(self, entity):
        entity_data = entity.to_dict()
        entity_data['events'] = []
        self.collection.insert_one(entity_data)

    def _get(self, id):
        entity_data = self.collection.find(id)
        if entity_data:
            entity = self.entity_class.from_dict(entity_data)
            return entity
        else:
            return None

    def _get_by_uuid(self, uuid):
        entity_data = self.collection.find_one({"uuid": uuid})
        if entity_data:
            entity = self.entity_class.from_dict(entity_data)
            return entity
        else:
            return None

    def _update(self, entity):
        self.collection.replace_one({"uuid": entity.uuid}, entity.to_dict())

    @staticmethod
    def make(
            entity_class,
            collection_name,
            db=mongodb.get_database(),
    ):
        return MongoRepository(entity_class, db[collection_name])


class MongoRecordingRepository(MongoRepository):

    def __init__(self, db):
        super().__init__(entity_class=Recording,
                         mongo_collection=db['recordings'])
        self.recordings_folder = os.path.join(
            get_file_storage_config()['ROOT_FOLDER'], "recordings")
        if not os.path.exists(self.recordings_folder):
            os.makedirs(self.recordings_folder)

    def create_new_recording(self, uuid, audio_video_file, audio_only_file,
                             video_only_file):

        audio_video_filepath = os.path.join(self.recordings_folder,
                                            audio_video_file.filename)
        audio_video_file.save(audio_video_filepath)

        audio_only_filepath = os.path.join(self.recordings_folder,
                                           audio_only_file.filename)
        audio_only_file.save(audio_only_filepath)

        video_only_filepath = os.path.join(self.recordings_folder,
                                           video_only_file.filename)
        video_only_file.save(video_only_filepath)

        combined_video_filepath = os.path.join(self.recordings_folder, f'{uuid}_combined')
        recording = Recording(
            uuid=uuid,
            audio_video_filepath=audio_video_filepath,
            audio_only_filepath=audio_only_filepath,
            video_only_filepath=video_only_filepath,
            combined_video_filepath=combined_video_filepath)

        recording.events.append(events.RecordingCreated(recording_uuid=uuid))

        self.add(recording)

        return recording


