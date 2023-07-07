__all__ = ("DependencyAnnotationMixin",)

from typing import Dict, Type

from ..base import BaseAnnotation


class DependencyAnnotationMixin:
    dependency_classes: Dict[str, Type["BaseAnnotation"]] = {}

    def get_dependency(self) -> Dict[str, "BaseAnnotation"]:
        return {
            name: an_cls(self.context, primary_outref=self.primary_outref)  # type: ignore
            for name, an_cls in self.dependency_classes.items()
        }
