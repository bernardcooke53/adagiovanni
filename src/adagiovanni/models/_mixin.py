from datetime import datetime
from typing import Any, Callable, Generator, Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.fields import ModelField


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[[Any], str], Any, Any]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> str:
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        if isinstance(v, str):
            return v
        raise TypeError(f"Invalid ObjectID: {v} {v!r} of type {type(v)}")

    @classmethod
    def __modify_schema__(cls, field: Optional[ModelField]) -> None:
        if field:
            field.update(type="string")  # type: ignore


class CreatedUpdatedDatesModelMixin(BaseModel):
    created_date: datetime = Field(default_factory=datetime.utcnow)
    updated_date: datetime = Field(default_factory=datetime.utcnow)


class IdModelMixin(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
