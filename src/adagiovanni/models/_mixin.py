from datetime import datetime
from typing import Any, Callable, Generator, Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.fields import ModelField


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[[Any], ObjectId], Any, Any]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise TypeError("Invalid ObjectID: %r" % v)
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field: Optional[ModelField]) -> None:
        if field:
            field.update(type="string")  # type: ignore


class CreatedUpdatedDatesModelMixin(BaseModel):
    created_date: datetime = Field(default_factory=datetime.utcnow)
    updated_date: datetime = Field(default_factory=datetime.utcnow)


class IdModelMixin(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
