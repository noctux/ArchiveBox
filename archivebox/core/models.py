__package__ = 'archivebox.core'

import uuid

from django.db import models

from ..util import parse_date
from ..index.schema import Link


class Snapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    url = models.URLField(unique=True)
    timestamp = models.CharField(unique=True, max_length=32, null=True, default=None)

    title = models.CharField(max_length=128, null=True, default=None)
    tags = models.CharField(max_length=256, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, default=None)

    keys = ('url', 'timestamp', 'title', 'tags', 'updated')


    def __repr__(self) -> str:
        return f'[{self.timestamp}] {self.url[:64]} ({self.title[:64]})'

    def __str__(self) -> str:
        return f'[{self.timestamp}] {self.url[:64]} ({self.title[:64]})'

    @classmethod
    def from_json(cls, info: dict):
        info = {k: v for k, v in info.items() if k in cls.keys}
        return cls(**info)

    def as_json(self, *args) -> dict:
        args = args or self.keys
        return {
            key: getattr(self, key)
            for key in args
        }

    def as_link(self) -> Link:
        return Link.from_json(self.as_json())

    @property
    def bookmarked(self):
        return parse_date(self.timestamp)

    @property
    def is_archived(self):
        return self.as_link().is_archived

    @property
    def num_outputs(self):
        return self.as_link().num_outputs

    @property
    def url_hash(self):
        return self.as_link().url_hash

    @property
    def base_url(self):
        return self.as_link().base_url

    @property
    def link_dir(self):
        return self.as_link().link_dir


class SnapshotResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    snapshot = models.ForeignKey(Snapshot,on_delete=models.CASCADE)
    output = models.CharField(max_length=128, null=True, default=None)
    status = models.CharField(max_length=128, null=True, default=None)

    cmd = models.CharField(max_length=512, null=True, default=None)
    pwd = models.CharField(max_length=128, null=True, default=None)
    cmd_version = models.CharField(max_length=128, null=True, default=None)
    cmd_hash = models.CharField(max_length=64, null=True, default=None)
    
    start_ts = models.DateTimeField(null=True, default=None)
    end_ts = models.DateTimeField(null=True, default=None)

    @property
    def output_hash(self):
        raise NotImplementedError
