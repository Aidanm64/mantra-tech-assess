# pylint: disable=attribute-defined-outside-init
from __future__ import annotations

import abc

import pymongo

from tech_assess import config
from tech_assess.adapters import mongodb
from tech_assess.adapters.repository import MongoRecordingRepository


class UnitOfWork(abc.ABC):
    recordings: Repository

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for recordings in self.recordings.seen:
            while recordings.events:
                yield recordings.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


def DEFAULT_MONGO_CLIENT_FACTORY():
    client = pymongo.MongoClient(config.get_mongo_url())
    return client


class MongoUnitOfWork(UnitOfWork):

    def __init__(self,
                 mongo_db_factory=mongodb.get_database):
        self.mongo_db_factory = mongo_db_factory

    def __enter__(self) -> UnitOfWork:
        self.db = self.mongo_db_factory()
        self.recordings = MongoRecordingRepository(
            db=self.db)
        return self

    def __exit__(self, *args):
        self.rollback()

    def _commit(self):
        pass

    def rollback(self):
        pass
