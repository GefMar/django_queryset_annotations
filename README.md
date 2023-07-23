# django_queryset_annotations

The `django_queryset_annotations` library provides a way to add annotations to Django querysets. Annotations are additional fields that are calculated on the fly and added to the queryset results. This can be particularly useful when you want to add computed fields to your models without having to modify the underlying database schema.

## Installation

You can install `django_queryset_annotations` via pip:

```bash
pip install queryset-annotations
```

## Usage

To use the `django_queryset_annotations` library, you first need to create an annotation class. An annotation class is a subclass of the `BaseAnnotation` class. The `BaseAnnotation` class provides a number of methods that you can use to define the annotation, such as the `name`, `output_field`, and `get_expression()` methods.

### Example

Consider the following models:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

You can create an annotation class to count the number of books for each author:

```python
from django.db import models
from queryset_annotations.base import BaseAnnotation

class BookCountAnnotation(BaseAnnotation):
    name = "book_count"
    output_field = models.IntegerField()

    def get_expression(self):
        return models.Count("books", distinct=True)
```

Then, create a proxy model for the `Author` model:

```python
from queryset_annotations.proxy.model import BaseProxyModel

class AuthorProxyModel(BaseProxyModel):
    book_count = BookCountAnnotation()

    class Meta:
        model = Author
```

You can now use this proxy model in your serializers and viewsets:

```python
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProxyModel
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorViewSet(ModelViewSet):
    queryset = AuthorProxyModel.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

With this setup, when you retrieve an author from the API, you will also get the count of books they have written.

## Advanced Usage

The `django_queryset_annotations` library also provides a `BaseContextManager` and an `AnnotatedQuerysetMixin` for more advanced use cases. The `BaseContextManager` can be used to manage the context of the annotation, and the `AnnotatedQuerysetMixin` can be used to automatically annotate the queryset in a viewset.

Here is an example of how to use these features:

```python
from django.db import models
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from annotation.models import Author, Book
from queryset_annotations.base import BaseAnnotation, BaseContextManager
from queryset_annotations.drf.views import AnnotatedQuerysetMixin
from queryset_annotations.proxy.model import BaseProxyModel

class BookCountAnnotation(BaseAnnotation):
    name = "book_count"
    output_field = models.IntegerField()

    def get_expression(self, *, context_manager: BaseContextManager = None):
        return models.Count("books", distinct=True)


class AuthorProxyModel(BaseProxyModel):
    book_count = BookCountAnnotation()

    class Meta:
        model = Author


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AuthorProxyModel
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorViewSet(AnnotatedQuerysetMixin, ModelViewSet):
    annotation_context_class = BaseContextManager
    annotated_model = AuthorProxyModel
    serializer_class = AuthorSerializer

    def get_queryset(self):
        context_manager = self.annotation_context_class(self.get_serializer_context())
        return self.queryset.get_annotated_queryset(context_manager=context_manager)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

In this example, the `AuthorViewSet` uses the `AnnotatedQuerysetMixin` and a `BaseContextManager` to automatically annotate the queryset with the book count.

## Conclusion

The `django_queryset_annotations` library provides a powerful and flexible way to add computed fields to your Django models. Whether you need to add simple counts or more complex calculations, this library can help you keep your code clean and maintainable.
