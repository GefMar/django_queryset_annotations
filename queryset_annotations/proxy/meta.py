__all__ = ("MetaProxyModel",)

from ..base.abstract_annotation import BaseAnnotation


class MetaProxyModel(type):
    def __new__(cls, name, bases, attrs):
        expression = {}
        annotations = {}
        for field_name, attr in attrs.items():
            if isinstance(attr, BaseAnnotation):
                expression[field_name] = attr.get_expression()
                annotations[field_name] = attr
                attrs[field_name] = attr.output_field
        attrs["_annotations"] = annotations
        attrs["objects"] = attrs["Meta"].model.objects.annotate(**expression)
        return super().__new__(cls, name, bases, attrs)
