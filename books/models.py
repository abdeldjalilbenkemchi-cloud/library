from django.db import models


class Book(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        db_table = 'books_book'