from mongoengine import DateTimeField, connect, ReferenceField, DynamicDocument
from pymongo import InsertOne
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


class BaseModel(DynamicDocument):
    created_at = DateTimeField(default=datetime.now)

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
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, dict):
                self._convert_object_ids_to_strings(value)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        self._convert_object_ids_to_strings(item)
                    if isinstance(item, ObjectId):
                        value[index] = str(item)
                    if isinstance(item, datetime):
                        value[index] = item.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def create(cls, data: dict, to_json=False):
        """
        This function is used to create the record.
        :param data: Data to create the record
        :param to_json: Flag to get response in json
        :param extend:
        :return: Created document
        """
        record = cls(**data)
        record.save(validate=False)
        if to_json:
            return record.to_json()
        return record

    @classmethod
    def add_created_at(cls, data):
        data["created_at"] = datetime.now()
        return data

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
    def bulk_write(cls, data: list) -> int:
        insert_operations = [InsertOne(cls.add_created_at(d)) for d in data]
        bulk_write_result = cls._get_collection().bulk_write(insert_operations)
        return bulk_write_result.inserted_count

    @classmethod
    def check_if_all_exists(cls, object_ids: list[ObjectId]) -> bool:
        return cls.objects(id__in=object_ids).count() == len(object_ids)

    @classmethod
    def get_all(cls) -> list:
        all_records = cls.objects()
        return [record.to_json() for record in all_records]

    @classmethod
    def get_objects_with_filter(cls, only_first=None, **filters):
        filtered_records = cls.objects(**filters)
        if only_first:
            record = filtered_records.first()
            if record:
                return record.to_json()
        return [record.to_json() for record in filtered_records]

    @classmethod
    def get_distinct(cls, field: str):
        return cls.objects.distinct(field)

    @classmethod
    def get_distinct_with_filters(cls, field: str, **filters):
        return cls.objects(**filters).distinct(field)

    @classmethod
    def get_reference_fields(cls):
        return [field_name for field_name, field in cls._fields.items() if isinstance(field, ReferenceField)]

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

        queryset = cls.objects(*filters)
        if return_all:
            if to_json:
                return [result.to_json() for result in queryset]
        if to_json:
            return queryset.first().to_json()
        return queryset.first()

