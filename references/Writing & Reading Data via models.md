# Writing & Reading Data via models.py in Django


### 1. Install dataclasses
```
pip install dataclasses
```

### 2. Data in a Python Class

```python
from dataclasses import dataclass

@dataclass
class BlogPost:
    title: str
    content: str
```

```python
obj = BlogPost()
```

```python
obj = BlogPost(title='Hello World', content='This is awesome')
```


### 3. Data in a Django Model Class

```python
# models.py

from django.db import models


class Article(models.Model):
    title = models.TextField()
    content = models.TextField()
```


#### Writing
```python
obj = Article(title='Hello World', content='This is awesome')
obj.save()
print(obj.id)
```
or

```python
obj2 = Article.objects.create(title='Hello World Again', content='This is awesome')
print(obj2.id)
```

#### Reading

```python
obj = Article.objects.get(id=1)
```