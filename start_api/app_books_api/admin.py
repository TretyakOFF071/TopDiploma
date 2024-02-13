from django.contrib import admin
from .models import Author, Book
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):

    model = Author
    list_display = ['first_name', 'last_name', 'birthday']

class BookAdmin(admin.ModelAdmin):

    model = Book
    list_display = ['name', 'author', 'publish_date']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
