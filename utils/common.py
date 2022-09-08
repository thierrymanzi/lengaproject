# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 11:14:03
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 11:21:59
# Project: lenga

import os
import uuid
from urllib.parse import urljoin

import pandas as pd
from decouple import config
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class LengaError(Exception):
    pass


class BaseModel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        ordering = ['-modified']


class FileExport:
    def __init__(
        self, data,
        file_name=('%s_%s' % (uuid.uuid4(), timezone.now())),
        file_dir='/projects/lenga/media/tmp/'
    ):
        self.data = data
        self.dir = file_dir
        self.file_name = file_name

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, name):
        path, ext = os.path.splitext(name)
        if not ext or ext != '.csv':
            name = '%s.csv' % path
        self._file_name = name

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, d):
        if not os.path.isdir(d):
            os.makedirs(d)
        self._dir = d

    def _get_file_path(self):
        return os.path.join(self.dir, self.file_name)

    def file_url(self):
        path = self._get_file_path()
        if not os.path.exists(path):
            raise LengaError(
                'Export file does not exist. Did you forget to create the file?')
        return urljoin(
            '%s:%s' % (config('EXPORT_HOST_URL'), config('EXPORT_HOST_PORT')),
            os.path.join('exports/', self.file_name)
        )

    def generate_csv(self):
        try:
            df = pd.DataFrame.from_records(self.data)
            df.to_csv(self._get_file_path(), index=False)
        except Exception:
            pass

    def file_export(self):
        self.generate_csv()
        return self.file_url()
