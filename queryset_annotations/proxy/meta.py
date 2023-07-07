__all__ = ("MetaProxyModel",)

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
        for field_name, attr in attrs.items():
            if isinstance(attr, BaseAnnotation):
                expressions[field_name] = attr.get_expression()
                annotations[field_name] = attr
                attrs[field_name] = attr.output_field
        attrs["_annotations"] = annotations
        attrs["objects"] = cls.make_manager(attrs["Meta"].model.objects.__class__, expressions)()
        attrs["objects"].model = attrs["Meta"].model

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def make_manager(cls, original_manager, expressions):
        def get_queryset(self):
            return super(self.__class__, self).get_queryset().annotate(**expressions)

        return type(f"Annotated{original_manager.__name__}", (original_manager,), {"get_queryset": get_queryset})
