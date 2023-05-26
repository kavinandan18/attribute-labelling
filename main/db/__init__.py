from mongoengine import Document, DateTimeField, connect
from datetime import datetime
from bson.objectid import ObjectId
import json
from mongoengine.queryset.visitor import Q
import os
from config import config_by_name

config = config_by_name[os.getenv("FLASK_ENV") or "dev"]

connect(
    db='attribute_labelling',
    host='localhost',
    port=27017
)


class BaseModel(Document):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=None, on_update=datetime.now)

    meta = {
        'abstract': True
    }

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        self._convert_object_ids_to_strings(data)
        return json.loads(json.dumps(data))

    def _convert_object_ids_to_strings(self, data):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = str(datetime)
            elif isinstance(value, dict):
                self._convert_object_ids_to_strings(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._convert_object_ids_to_strings(item)

    @classmethod
    def create(cls, data: dict, to_json=False):
        """
        This function is used to create the record.
        :param data: Data to create the record
        :return: Created document
        """
        record = cls(**data)
        record.save()
        if to_json:
            return record.to_json()
        return record

    def update(self, data: dict):
        """
        This function is used to update the record.
        :param data: Data to update the record
        """
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.save()

    @classmethod
    def delete(cls, **filters):
        """
        This function is used to delete the records based on filters.
        :param filters: Filters to match the records to delete
        """
        cls.objects(**filters).delete()

    @classmethod
    def filter(cls, filters_dict, return_all=False, to_json=False):
        filters = []

        for operator, conditions in filters_dict.items():
            if operator == "eq":
                for field, value in conditions.items():
                    filters.append(Q(**{field: value}))
            elif operator == "op_or":
                or_filters = [Q(**{field: value}) for field, value in conditions.items()]
                or_filter = or_filters[0]
                for i in range(1, len(or_filters)):
                    or_filter |= or_filters[i]
                filters.append(or_filter)
            # Add more operator conditions as needed

        queryset = cls.objects(*filters)
        if return_all:
            if to_json:
                return [result.to_json() for result in queryset]
        if to_json:
            return queryset.first().to_json()
        return queryset.first()
