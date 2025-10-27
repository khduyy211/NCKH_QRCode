from django.db import models

# Create your models here.
class Book_Shelf(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Compartment(models.Model):
    shelf = models.ForeignKey(Book_Shelf, related_name='compartments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    row_number = models.IntegerField()
    column_number = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Shelf: {self.shelf.name})"

class Book_Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    shelf = models.ForeignKey(Book_Shelf, related_name='books', on_delete=models.CASCADE)
    compartment = models.ForeignKey(Compartment, related_name='books', on_delete=models.CASCADE)
    book_type = models.ForeignKey(Book_Type, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} by {self.author} (Shelf: {self.shelf.name}, Compartment: {self.compartment.name})"