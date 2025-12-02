from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from ..models import Book


class BookRepository :
    def get_all(self):
        try :
            return Book.objects.all().order_by('title')
        except Exception:
            print(f"Error getting all books : {Exception}")
            return Book.objects.none()
        pass

    def get_by_id(self,book_id):
        try:
            return Book.objects.get(pk=book_id)
        except ObjectDoesNotExist:
            return None
        except  Exception:
             print(f"Error getting book_id : {Exception}")
             return None



    def get_available(self):
        try : 
            return Book.objects.filter(available=True).order_by('title')
        except Exception:
             print(f"Error getting filtered books: {Exception}")
             return None
        
    def search_by_title(self,query):
        if not query:
            return Book.objects.none()
        try:
            return Book.objects.filter(title__icontains=query).order_by("title")
        
        except Exception:
             print(f"Error searching_by_title '{query}': {Exception}")
             return Book.objects.none()
        
    def filter_by_author(self,author_name):
        if not author_name:
            return Book.objects.none()
        try :
            return Book.objects.filter(author__icontains=author_name).order_by('title')
        except Exception:
             print(f"Error searching_by_author '{author_name}': {Exception}")
             return Book.objects.none()


    def create(self,data):
        try: 
            book=Book.objects.create(**data)
            return book
        
        except IntegrityError:
            print(f"Integrity Error creating book: {IntegrityError}")
            return None
        
        except Exception :
            print(f"Unexpected error creating book: {Exception}")
            return None
        
    def update(self, book_id,data):
        try:
            book = self.get_by_id(book_id)
            if not book:
                print ('book not found')
                return None
            for key, value in data.items():
                setattr(book,key,value)

            book.save()
            return book
        
        except IntegrityError:
            print(f"Integrity Error updating book {book_id}: {IntegrityError}")
            return None
        
        except Exception :
            print(f"Unexpected error updating book {book_id}: {Exception}")
            return None
        
    def delete(self,book_id):
        book = self.get_by_id(book_id)
        try:
            if not book:
                print ('book not found')
                return False

            book.delete()
        
        except Exception :
            print(f"Unexpected error deleting book {book_id}: {Exception}")
            return False
        
    def get_by_isbn(self, isbn):
        if not isbn :
            raise ValueError("isbn cannot be empty")
        try :

            return Book.objects.get(isbn=isbn)
        
        except ObjectDoesNotExist:
            return None
        except Exception:
            print(f"Unexpected error isbn : {isbn} not found: {Exception}")
            return None
        