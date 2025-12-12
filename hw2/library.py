class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True
    
    def get_info(self):
        return f"«{self.title}», {self.author}, {self.year}"
    
    def borrow(self):
        if self.is_available:
            self.is_available = False
            return True
        return False
    
    def return_book(self):
        self.is_available = True


class TextBook(Book):
    def __init__(self, title, author, year, subject):
        super().__init__(title, author, year)
        self.subject = subject
    
    def get_info(self):
        return f"«{self.title}», {self.author}, {self.year} — предмет: {self.subject}"


class Library:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def find_books_by_author(self, author):
        result = []
        for book in self.books:
            if book.author == author:
                result.append(book)
        return result
    
    def get_available_books(self):
        result = []
        for book in self.books:
            if book.is_available:
                result.append(book)
        return result
    
    def borrow_book(self, title):
        for book in self.books:
            if book.title == title:
                if book.is_available:
                    book.borrow()
                    return True
                else:
                    return False
        return False

