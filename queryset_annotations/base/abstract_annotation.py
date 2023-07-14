__all__ = ("BaseAnnotation",)

from abc import ABC, abstractmethod
from typing import Any, Dict

from django.db import models


class BaseAnnotation(ABC):
    context: Dict[str, Any]
    primary_outref: models.OuterRef = models.OuterRef("pk")
    context = {}

    def __init__(self, context=None, primary_outref: models.OuterRef = None):
        if context is not None:
            self.context = context
        if primary_outref is not None:
            self.primary_outref = primary_outref

    @property
    @abstractmethod
    def name(self) -> str:
        ...  # noqa: WPS428

    @property
    @abstractmethod
    def output_field(self) -> models.Field:
        ...  # noqa: WPS428

    @abstractmethod
    def get_expression(self) -> models.expressions.BaseExpression:
        ...  # noqa: WPS428
