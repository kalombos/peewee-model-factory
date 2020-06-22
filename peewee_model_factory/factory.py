import random
import collections
import typing as t
import datetime as dt

import pytz
import peewee as pw
from playhouse.postgres_ext import DateTimeTZField, BinaryJSONField


class Counter(collections.Counter):
    def inc(self, element: str) -> int:
        self.update(**{element: 1})
        return self[element]


counter = Counter()


def char_enum_field_factory(field: pw.Field) -> str:
    first_choice = field.choices[0]
    first_value: str = first_choice[0]
    return first_value


def char_field_factory(field: pw.Field) -> str:
    value = counter.inc(field.name)
    return "%s%s" % (field.name, value)


def integer_field_factory(field: pw.Field) -> int:
    return counter.inc(field.name)


def json_field_factory(field: pw.Field) -> t.Dict[str, t.Any]:
    value = counter.inc(field.name)
    return {f"key{value}": f"value{value}"}


field_type_map = {
    pw.DateField: lambda _: dt.date.today(),
    pw.DateTimeField: lambda _: dt.datetime.now(),
    DateTimeTZField: lambda _: dt.datetime.utcnow().replace(tzinfo=pytz.utc),
    pw.CharField: char_field_factory,
    pw.TextField: char_field_factory,
    pw.IntegerField: integer_field_factory,
    pw.SmallIntegerField: integer_field_factory,
    pw.BooleanField: lambda _: False,
    pw.BigIntegerField: lambda _: random.randint(1, 9999999),
    BinaryJSONField: json_field_factory,
}

_missing = object()


class FieldNotFound(Exception):
    pass


def model_factory(
    model: t.Type[pw.Model],
    custom_field_type_map: t.Dict[t.Type[pw.Field], t.Callable[[pw.Field], t.Any]] = None,
    fill_nullable_values: bool = False,
    **kwargs: t.Any
) -> pw.Model:
    """Функция для быстрого создания моделей."""
    _field_type_map = field_type_map.copy()
    if custom_field_type_map is not None:
        _field_type_map.update(custom_field_type_map)

    nm = model()
    for field_name in kwargs:
        if field_name not in model._meta.fields:
            raise FieldNotFound(f'{model.__name__} has no "{field_name}" field')
    for field in model._meta.fields.values():
        field_name = field.name
        field_type = type(field)
        field_value = kwargs.get(field_name, _missing)
        if field_value is not _missing:
            pass
        elif field.primary_key or field.default:
            continue
        elif field.null and not fill_nullable_values:
            field_value = None
        elif field_type is pw.ForeignKeyField:
            field_value = model_factory(
                field.rel_model,
                custom_field_type_map=_field_type_map,
                fill_nullable_values=fill_nullable_values
            )
        else:
            field_factory = _field_type_map[field_type]
            field_value = field_factory(field)
        setattr(nm, field_name, field_value)
    nm.save(force_insert=True)
    return nm
