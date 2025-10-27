from django.contrib import admin
from demo_app.models import Book_Shelf, Compartment, Book_Type, Book
# Register your models here.
admin.site.register(Book_Shelf)
admin.site.register(Compartment)
admin.site.register(Book_Type)
admin.site.register(Book)