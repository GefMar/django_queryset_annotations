__all__ = ("BaseProxyModel",)

from django.db import models

from .meta import MetaProxyModel


class BaseProxyModel(metaclass=MetaProxyModel):
    objects: models.Manager

    class Meta:
        abstract = True
