# django_queryset_annotations
The queryset_annotations library provides a way to add annotations to Django querysets.
Annotations are additional fields that are calculated on the fly and added to the queryset results.

To use the queryset_annotations library, you first need to create an annotation class.
An annotation class is a subclass of the BaseAnnotation class.
The BaseAnnotation class provides a number of methods that you can use to define the annotation,
such as the name, output_field, and get_expression() methods.

## how to use django queryset annotations

example models.py
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

```

Create annotation class
```python
from django.db import models
from queryset_annotations.base import BaseAnnotation

class BookCountAnnotation(BaseAnnotation):
    name = "book_count"
    output_field = models.IntegerField()

    def get_expression(self):
        return models.Count("books", distinct=True)


```

create proxy model for Author
```python
from queryset_annotations.proxy.model import BaseProxyModel

class AuthorProxyModel(BaseProxyModel):
    book_count = BookCountAnnotation()

    class Meta:
        model = Author

```
use proxy model in serializers and viewsets
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
