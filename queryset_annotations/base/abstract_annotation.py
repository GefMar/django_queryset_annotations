__all__ = ("BaseAnnotation",)

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from django.db import models

from .context import BaseContextManager

_ContextType = Optional[Dict[str, Any]]
_ContextMakerType = Optional[Callable[[_ContextType], _ContextType]]


class BaseAnnotation(ABC):
    primary_outref: models.OuterRef = models.OuterRef("pk")

    def __init__(self, primary_outref: models.OuterRef = None, *, context_manager: BaseContextManager = None):
        if primary_outref is not None:
            self.primary_outref = primary_outref
        if context_manager is None:
            context_manager = BaseContextManager()
        self.context_manager = context_manager

    @property
    @abstractmethod
    def name(self) -> str:
        ...  # noqa: WPS428

    @property
    @abstractmethod
    def output_field(self) -> models.Field:
        ...  # noqa: WPS428

    @abstractmethod
    def get_expression(self, *, context_manager: Optional[BaseContextManager]) -> models.expressions.BaseExpression:
        ...  # noqa: WPS428
