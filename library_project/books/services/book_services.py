from ..repositories.repository import BookRepository

class BookService:
    def __init__(self):
        self.repo=BookRepository()

    def _format_success (self,message,data=None):
        return {"success":True,"message":message,"data":data}
    
    def _format_error (self,message,data=None):
        return {"success":False,"message":message,"data":data}

    def _validate_isbn_unique(self,isbn,exclude_id=None):
        if not isbn :
            return self._format_error('isbn required')
        
        book = self.repo.get_by_isbn(isbn)
        
        if exclude_id is not None:
            try:
                exclude_id = int(exclude_id)
            except ValueError:
                return self._format_error("invalid book ID format for update, expected Int value.")
            
        if book and (exclude_id is None or book.id != exclude_id):
            return self._format_error("this isbn already exists!")
        else :
            return self._format_success("this isbn is unique")

    def get_all_books(self):
        books=self.repo.get_all()
        if books :
            return self._format_success("all books retrieved succesfully", data=books)
        
    def get_book_by_id(self, book_id):
        book=self.repo.get_by_id(book_id)
        if book :
            return self._format_success(f"book {book} with id : {book.id} retrieved succesfully", data=book)
        return self._format_error(f"book with id : {book_id} not found")
    
    def create_book(self,data):
        isbn = data.get("isbn")
        isbn_check = self._validate_isbn_unique(isbn)
        if not isbn_check['success'] : 
            return isbn_check
        new_book= self.repo.create(data)

        if new_book : 
            return self._format_success("book created",data=new_book)
        return self._format_error("Failed to created a new book")
        
    def update_book(self,book_id,data):
        if 'isbn' in data : 
            isbn_check= self._validate_isbn_unique(data['isbn'],exclude_id=book_id)
            if not isbn_check['success']:
                return isbn_check


        updated_book= self.repo.update(book_id,data)
        if updated_book:
            return self._format_success("book updated")
        return self._format_error(f"failed to update book {book_id}")
    
    def delete_book(self,book_id):
        try:
            success= self.repo.delete(book_id)
            if success :
                return self._format_success(f"Book {book_id} deleted")
            else:
                return self._format_error("book does not exist or and error occured")
        except Exception:
            return self._format_error(f'an error occured during deletion : {Exception}')

#Lazem n3awed nwelli liha 
    def search_books_by_title(self,query):
        if not query : 
            books=self.repo.get_all()
            return self._format_success(f"no title, all books have been retrieved instead",data=books)
        books = self.repo.search_by_title(query)
        
        return self._format_success(f"found {len(books)} matching {query}",data=books)
    
    def filter_books_by_author(self,author_name):
        if not author_name: 
            return self._format_error("author name must be provided")
        books=self.repo.filter_by_author(author_name)
        return self._format_success(f"found {len(books)} matching the author name :{author_name}",data=books)
    
    def get_available_books(self):
        books=self.repo.get_available()
        return self._format_success(f"found {len(books)} available books",data=books)