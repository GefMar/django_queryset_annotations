import typing

from queryset_annotations.base.context import BaseContextManager


def get_proxy_manager(manage_cls, annotations):
    class AnnotatedManager(manage_cls):  # noqa: WPS431
        _annotations = annotations

        @property
        def queryset(self):
            return self.get_queryset()

        def get_annotated_queryset(self, *, context_manager: typing.Optional[BaseContextManager] = None):
            queryset = self.get_queryset()
            annotation_dict = self._get_annotation_dict(context_manager=context_manager)
            return queryset.annotate(**annotation_dict)

        def _get_annotation_dict(self, *, context_manager):
            return {
                name: annotation.get_expression(context_manager=context_manager)
                for name, annotation in self._annotations.items()
            }

    return AnnotatedManager
