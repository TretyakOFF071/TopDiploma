from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(
        auto_now_add=False
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):

    name = models.CharField(max_length=30)
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=False)
    pagination_num = models.IntegerField()

    def __str__(self):
        return f'{self.name}'