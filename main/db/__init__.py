import json
import os
from datetime import datetime

from bson.objectid import ObjectId
from mongoengine import DateTimeField, DynamicDocument, connect

from config import config_by_name

config = config_by_name[os.getenv("FLASK_ENV") or "dev"]
connect(host=config["DATABASE_URI"])


class BaseModel(DynamicDocument):
    created_at = DateTimeField(default=datetime.now)

    meta = {"abstract": True}

    def to_json(self, *args, **kwargs) -> dict:
        """
        To convert data into json.
        """
        data = self.to_mongo(*args, **kwargs)
        self._convert_objects_ids_and_date_to_strings(data)
        return json.loads(json.dumps(data))

    def _convert_objects_ids_and_date_to_strings(self, data: dict):
        """
        To convert object ids and date values to string.
        :param data:
        """
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, dict):
                self._convert_objects_ids_and_date_to_strings(value)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        self._convert_objects_ids_and_date_to_strings(item)
                    if isinstance(item, ObjectId):
                        value[index] = str(item)
                    if isinstance(item, datetime):
                        value[index] = item.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def create(cls, data: dict, to_json=False):
        """
        To create the record.
        :param data: Data to create the record
        :param to_json: Flag to get response in json
        :return: Created document
        """
        record = cls(**data)
        record.save(validate=False)
        if to_json:
            return record.to_json()
        return record

    def update(self, data: dict):
        """
        To update the record.
        :param data: Data to update the record
        """
        for k, v in data.items():
            setattr(self, k, v)
        self.save()

    def replace(self, data: dict):
        """
        To replace the record.
        :param data:
        """
        for field_name in self._fields_ordered:
            if field_name != "id" and field_name not in data:
                delattr(self, field_name)

        for k, v in data.items():
            setattr(self, k, v)

        self.save()

    @classmethod
    def get_all(cls) -> list:
        """
        To get all records.
        :return:
        """
        all_records = cls.objects()
        return [record.to_json() for record in all_records]

    @classmethod
    def get_objects_with_filter(cls, only_first=None, **filters) -> list:
        """
        To get objects with filter
        :param only_first:
        :param filters:
        :return:
        """
        filtered_records = cls.objects(**filters)
        if only_first:
            record = filtered_records.first()
            if record:
                return record.to_json()
        return [record.to_json() for record in filtered_records]

    @classmethod
    def get_distinct(cls, field: str) -> list:
        """
        To get distinct of a field.
        :param field:
        :return:
        """
        return cls.objects.distinct(field)

    @classmethod
    def get_distinct_with_filters(cls, field: str, **filters) -> list:
        """
        To get distinct of a with filters.
        :param field:
        :param filters:
        :return:
        """
        return cls.objects(**filters).distinct(field)
