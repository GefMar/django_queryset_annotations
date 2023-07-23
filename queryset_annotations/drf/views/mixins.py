__all__ = ("AnnotatedQuerysetMixin",)

from typing import Type

from queryset_annotations import BaseContextManager, BaseProxyModel
from queryset_annotations.tools import classproperty


class AnnotatedQuerysetMixin:
    annotated_model: BaseProxyModel
    annotation_context_class: Type[BaseContextManager] = BaseContextManager

    @classproperty
    def queryset(cls):  # noqa: N805
        return cls.annotated_model.objects

    def get_queryset(self):
        return self.queryset.get_annotated_queryset()
