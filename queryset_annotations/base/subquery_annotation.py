__all__ = ("SubqueryAnnotation",)

from abc import ABC, abstractmethod
from typing import Tuple

from django.db import models

from .abstract_annotation import BaseAnnotation


class SubqueryAnnotation(BaseAnnotation, ABC):
    @property
    @abstractmethod
    def queryset(self) -> models.QuerySet:
        ...  # noqa: WPS428

    @property
    @abstractmethod
    def output_field_name(self) -> str:
        ...  # noqa: WPS428

    @property
    @abstractmethod
    def filters(self) -> Tuple[models.Q, ...]:
        ...  # noqa: WPS428

    def get_expression(self) -> models.Subquery:
        return models.Subquery(self.queryset.filter(*self.filters).values(self.output_field_name)[:1])
