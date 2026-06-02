from typing import TypeVar, Optional
from pydantic import BaseModel
from src.database import Base

DbModelType = TypeVar("DbModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: Optional[type[DbModelType]] = None
    schema: Optional[type[SchemaType]] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        if cls.schema is None:
            raise ValueError("schema not set")
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        if cls.db_model is None:
            raise ValueError("db_model not set")
        return cls.db_model(**data.model_dump())