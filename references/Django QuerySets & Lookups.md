Basic Django QuerySet Reference Guide

## `.all()` Get everything
```python
from articles.models import Article

qs = Article.objects.all()
```


## `.filter()` Filter by a field

```
qs = Article.objects.filter(title='Hello World')
```




## `__exact` Exact match
```
qs = Article.objects.filter(title__exact='Hello World')
```

## `__iexact` Case-insensitve match

```
qs = Article.objects.filter(title__iexact='HELLO World')
```


## `__icontains` Case-insensitive contains

```
qs = Article.objects.filter(title__icontains='World')
```

## `__contains` Case-sensitive contains

```
qs = Article.objects.filter(title__contains='wOrld')
```


## `__in` Check inside a given iterable

```
ids = [15, 16, 20]
qs = Article.objects.filter(id__in=ids)
```