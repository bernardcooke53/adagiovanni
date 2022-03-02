# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
mixins

These models are mixins to be composed with other models,
that allow common attributes to be added without re-implementing
all the JSON serde & parsing associated.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Generator

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    """
    MongoDB returns its Ids in a field "_id", but as a BSON
    encoded unique identifier that isn't JSON serializable.
    This subclass is a wrapper which supplies the minimal
    interface for Pydantic to recognize it as a type and
    represent it correctly in the OpenAPI documentation, as
    well as to convert it to the correct format to push back
    to the database.
    """

    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[[Any], PyObjectId], Any, Any]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> PyObjectId:
        if not cls.is_valid(v):
            raise ValueError(f"Invalid ObjectID: {v} {v!r} of type {type(v)}")
        return cls(v)

    @classmethod
    def __modify_schema__(cls, f_schema: dict[str, Any]) -> None:
        f_schema.update(type="string")


class IdModelMixin(BaseModel):
    """
    We encapsulate the difficulties of handling the MongoDB _id
    implementation by creating a mixin model, so if we want to
    use the ID field in another model we can add this class to
    the inheritance hierarchy and this will be set up for us.
    """

    id: PyObjectId | None = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreatedUpdatedDatesModelMixin(BaseModel):
    """
    These are needed to ensure that we have JSON
    serializable representations of the date fields.

    Using this class as a mixin will add these to the
    subclassing model, which is more often than not
    going to be a useful addition to the documents we're
    creating and reading back.

    Mongo seems to truncate to the millisecond, so by
    truncating the dates in this model we eliminate some of
    the headaches in checking the correctness of the data -
    by storing it in Mongo we are only going to lose that
    anyway.
    """

    created_date: datetime = Field(
        default_factory=lambda: datetime.utcnow().replace(microsecond=0)
    )
    updated_date: datetime = Field(
        default_factory=lambda: datetime.utcnow().replace(microsecond=0)
    )
