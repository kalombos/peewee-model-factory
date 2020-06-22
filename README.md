peewee_model_factory
====================


#### No time? Ready to use?

```
pip install peewee-model-factory
```

```python
from peewee_model_factory import model_factory
from model import Author, Book
 
author = model_factory(Author, fill_nullable_values=True)
book = model_factory(Book, author=author)

```

#### Need custom type generation?

```python
import peewee as pw
from peewee_model_factory import model_factory

def char_field_factory(field: pw.Field) -> str:
    return f"my char value for field: {field.name}"


field_type_map = {
    pw.CharField: char_field_factory,
}


def my_custom_model_factory(*args, **kwargs) -> pw.Model:
    return model_factory(*args, custom_field_type_map=field_type_map, **kwargs) 

```

#### Want to use with peewee-async?

```python
import peewee as pw
from peewee_model_factory import model_factory
from peewee_async import Manager

manager = Manager(...)


def my_custom_model_factory(*args, **kwargs) -> pw.Model:
    with manager.allow_sync():
        return model_factory(*args, **kwargs) 

```


# Description
A library to create peewee model instances for testing. 
The project creation has been inspired by [django-dynamic-fixture](https://github.com/paulocheque/django-dynamic-fixture)
and [peewee-fake_fixtures](https://github.com/niedbalski/peewee-fake_fixtures) projects.

#### Features
* Recursevely creating models for foreign fields
* An option for filling nullable values
* Easy customization if you need to extend or change generation for types of peewee fields

#### Possible inconvenience
* The project has no tests.
* Not all field types of peeweee has factory function in the project. You have to write custom one if you want to use them

 