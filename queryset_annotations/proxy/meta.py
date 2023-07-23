__all__ = ("MetaProxyModel",)

from copy import copy

from ..base.abstract_annotation import BaseAnnotation
from .manager import get_proxy_manager


class MetaProxyModel(type):
    __manager_cls = None
    __objects = None
    _annotations: dict[str, BaseAnnotation] = {}

    def __new__(mcls, name, bases, attrs):
        if getattr(attrs["Meta"], "abstract", False):
            return super().__new__(mcls, name, bases, attrs)
        return mcls.make_proxy_model(name, bases, attrs)

    @classmethod
    def make_proxy_model(mcls, name, bases, attrs):
        annotations = {}
        meta = copy(attrs["Meta"].model._meta)  # noqa: WPS437
        meta_fields = list(meta.fields)
        filtered_attrs = filter(lambda obj: isinstance(obj[1], BaseAnnotation), attrs.items())
        for field_name, attr in filtered_attrs:
            output_field = mcls.__make_output_field(attr.output_field, field_name)
            meta_fields.append(output_field)
            annotations[field_name] = attr
        meta.fields = type(meta.fields)(meta_fields)
        meta.concrete_model._meta = meta  # noqa: WPS437
        attrs["_meta"] = meta
        attrs["_annotations"] = annotations

        return super().__new__(mcls, name, bases, attrs)

    @property
    def manager_cls(cls):
        if cls.__manager_cls is None:
            cls.__manager_cls = get_proxy_manager(
                cls.Meta.model.objects.__class__,
                cls._annotations,
            )
        return cls.__manager_cls

    @property
    def objects(cls):
        if cls.__objects is None:
            cls.__objects = cls.manager_cls()
            cls.__objects.model = cls.Meta.model

        return cls.__objects

    @property
    def _default_manager(cls):
        return cls.objects

    @classmethod
    def __make_output_field(mcls, output_field, field_name):
        output_field.attname = field_name
        output_field.name = field_name
        output_field.editable = False
        output_field.concrete = False
        output_field.column = None
        return output_field
