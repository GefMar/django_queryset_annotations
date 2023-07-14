__all__ = ("MetaProxyModel",)

from copy import copy

from ..base.abstract_annotation import BaseAnnotation


class MetaProxyModel(type):
    def __new__(cls, name, bases, attrs):
        if getattr(attrs["Meta"], "abstract", False):
            return super().__new__(cls, name, bases, attrs)
        return cls.make_proxy_model(name, bases, attrs)

    @classmethod
    def make_proxy_model(cls, name, bases, attrs):
        expressions = {}
        annotations = {}
        meta = copy(attrs["Meta"].model._meta)  # noqa: WPS437
        meta_fields = list(meta.fields)
        for field_name, attr in attrs.items():
            if isinstance(attr, BaseAnnotation):
                attr.output_field.attname = field_name
                attr.output_field.name = field_name
                attr.output_field.editable = False
                attr.output_field.concrete = False
                attr.output_field.column = None
                meta_fields.append(attr.output_field)
                expressions[field_name] = attr.get_expression()
                annotations[field_name] = attr
        meta.fields = type(meta.fields)(meta_fields)
        meta.concrete_model._meta = meta  # noqa: WPS437
        attrs["_meta"] = meta
        attrs["_annotations"] = annotations
        attrs["objects"] = cls.make_manager(attrs["Meta"].model.objects.__class__, expressions)()
        attrs["_default_manager"] = attrs["objects"]
        attrs["objects"].model = attrs["Meta"].model

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def make_manager(cls, original_manager, expressions):
        def get_queryset(self):
            return super(self.__class__, self).get_queryset().annotate(**expressions)

        return type(f"Annotated{original_manager.__name__}", (original_manager,), {"get_queryset": get_queryset})
