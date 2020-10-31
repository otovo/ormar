import datetime
import decimal
import uuid
from typing import Any, Optional, Type

import pydantic
import sqlalchemy

from ormar import ModelDefinitionError  # noqa I101
from ormar.fields import sqlalchemy_uuid
from ormar.fields.base import BaseField  # noqa I101


def is_field_nullable(
    nullable: Optional[bool], default: Any, server_default: Any
) -> bool:
    if nullable is None:
        return default is not None or server_default is not None
    return nullable


class ModelFieldFactory:
    _bases: Any = (BaseField,)
    _type: Any = None
    _pydantic_type: Any = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Type[BaseField]:  # type: ignore
        cls.validate(**kwargs)

        default = kwargs.pop("default", None)
        server_default = kwargs.pop("server_default", None)
        nullable = kwargs.pop("nullable", None)

        namespace = dict(
            __type__=cls._type,
            __pydantic_type__=cls._pydantic_type,
            name=kwargs.pop("name", None),
            primary_key=kwargs.pop("primary_key", False),
            default=default,
            server_default=server_default,
            nullable=is_field_nullable(nullable, default, server_default),
            index=kwargs.pop("index", False),
            unique=kwargs.pop("unique", False),
            pydantic_only=kwargs.pop("pydantic_only", False),
            autoincrement=kwargs.pop("autoincrement", False),
            column_type=cls.get_column_type(**kwargs),
            choices=set(kwargs.pop("choices", [])),
            **kwargs
        )
        return type(cls.__name__, cls._bases, namespace)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:  # pragma no cover
        return None

    @classmethod
    def validate(cls, **kwargs: Any) -> None:  # pragma no cover
        pass


class String(ModelFieldFactory):
    _type = str
    _pydantic_type = pydantic.ConstrainedStr

    def __new__(  # type: ignore # noqa CFQ002
        cls,
        *,
        allow_blank: bool = True,
        strip_whitespace: bool = False,
        min_length: int = None,
        max_length: int = None,
        curtail_length: int = None,
        regex: str = None,
        **kwargs: Any
    ) -> Type[BaseField]:  # type: ignore
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        kwargs["allow_blank"] = kwargs.get("nullable", True)
        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.String(length=kwargs.get("max_length"))

    @classmethod
    def validate(cls, **kwargs: Any) -> None:
        max_length = kwargs.get("max_length", None)
        if max_length is None or max_length <= 0:
            raise ModelDefinitionError(
                "Parameter max_length is required for field String"
            )


class Integer(ModelFieldFactory):
    _type = int
    _pydantic_type = pydantic.ConstrainedInt

    def __new__(  # type: ignore
        cls,
        *,
        minimum: int = None,
        maximum: int = None,
        multiple_of: int = None,
        **kwargs: Any
    ) -> Type[BaseField]:
        autoincrement = kwargs.pop("autoincrement", None)
        autoincrement = (
            autoincrement
            if autoincrement is not None
            else kwargs.get("primary_key", False)
        )
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        kwargs["ge"] = kwargs["minimum"]
        kwargs["le"] = kwargs["maximum"]
        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.Integer()


class Text(ModelFieldFactory):
    _type = str
    _pydantic_type = pydantic.ConstrainedStr

    def __new__(  # type: ignore
        cls, *, allow_blank: bool = True, strip_whitespace: bool = False, **kwargs: Any
    ) -> Type[BaseField]:
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        kwargs["allow_blank"] = kwargs.get("nullable", True)
        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.Text()


class Float(ModelFieldFactory):
    _type = float
    _pydantic_type = pydantic.ConstrainedFloat

    def __new__(  # type: ignore
        cls,
        *,
        minimum: float = None,
        maximum: float = None,
        multiple_of: int = None,
        **kwargs: Any
    ) -> Type[BaseField]:
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        kwargs["ge"] = kwargs["minimum"]
        kwargs["le"] = kwargs["maximum"]
        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.Float()


class Boolean(ModelFieldFactory):
    _type = bool
    _pydantic_type = bool

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.Boolean()


class DateTime(ModelFieldFactory):
    _type = datetime.datetime
    _pydantic_type = datetime.datetime

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.DateTime()


class Date(ModelFieldFactory):
    _type = datetime.date
    _pydantic_type = datetime.date

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.Date()


class Time(ModelFieldFactory):
    _type = datetime.time
    _pydantic_type = datetime.time

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.Time()


class JSON(ModelFieldFactory):
    _type = pydantic.Json
    _pydantic_type = pydantic.Json

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.JSON()


class BigInteger(Integer):
    _type = int
    _pydantic_type = pydantic.ConstrainedInt

    def __new__(  # type: ignore
        cls,
        *,
        minimum: int = None,
        maximum: int = None,
        multiple_of: int = None,
        **kwargs: Any
    ) -> Type[BaseField]:
        autoincrement = kwargs.pop("autoincrement", None)
        autoincrement = (
            autoincrement
            if autoincrement is not None
            else kwargs.get("primary_key", False)
        )
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        kwargs["ge"] = kwargs["minimum"]
        kwargs["le"] = kwargs["maximum"]
        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.BigInteger()


class Decimal(ModelFieldFactory):
    _type = decimal.Decimal
    _pydantic_type = pydantic.ConstrainedDecimal

    def __new__(  # type: ignore # noqa CFQ002
        cls,
        *,
        minimum: float = None,
        maximum: float = None,
        multiple_of: int = None,
        precision: int = None,
        scale: int = None,
        max_digits: int = None,
        decimal_places: int = None,
        **kwargs: Any
    ) -> Type[BaseField]:
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        kwargs["ge"] = kwargs["minimum"]
        kwargs["le"] = kwargs["maximum"]

        if kwargs.get("max_digits"):
            kwargs["scale"] = kwargs["max_digits"]
        elif kwargs.get("scale"):
            kwargs["max_digits"] = kwargs["scale"]

        if kwargs.get("decimal_places"):
            kwargs["precision"] = kwargs["decimal_places"]
        elif kwargs.get("precision"):
            kwargs["decimal_places"] = kwargs["precision"]

        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        precision = kwargs.get("precision")
        scale = kwargs.get("scale")
        return sqlalchemy.DECIMAL(precision=precision, scale=scale)

    @classmethod
    def validate(cls, **kwargs: Any) -> None:
        precision = kwargs.get("precision")
        scale = kwargs.get("scale")
        if precision is None or precision < 0 or scale is None or scale < 0:
            raise ModelDefinitionError(
                "Parameters scale and precision are required for field Decimal"
            )


class UUID(ModelFieldFactory):
    _type = uuid.UUID
    _pydantic_type = uuid.UUID

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy_uuid.UUID()
