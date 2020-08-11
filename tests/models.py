import peewee as pw

db = pw.PostgresqlDatabase(
    database="pw-model-factory",
    user="pw-model-factory",
    password="pw-model-factory",
    host="localhost"
)


class Author(pw.Model):
    class Meta:
        database = db

    name = pw.CharField()
    last_name = pw.CharField()
    age = pw.IntegerField()


class Book(pw.Model):
    class Meta:
        database = db

    title = pw.CharField()
    author = pw.ForeignKeyField(Author)
    rating = pw.IntegerField()
    requests = pw.IntegerField(default=0)

