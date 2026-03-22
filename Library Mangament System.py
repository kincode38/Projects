#library Management System
class Book:
    def __init__(self, title: str,author: str):
        self.title = title
        self.author = author
        self.is_borrowed = False
    def display_info(self) -> None:
        status ="Available" if not self.is_borrowed else "Borrowed"
        print(f"Title: {self.title}, Author: {self.author}, Status: {status}")

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str) -> None:
        new_book = Book(title, author)
        self.books.append(new_book)
        print(f"Book '{new_book.title}' by {new_book.author} has been added to the library.")

    # View all books
    def view_books(self) -> None:
        if not self.books:
            print("No books in the library.")
        else:
            print("\n---Library Books---")
            for book in self.books:
                book.display_info()

    # Borrow a book
    def borrow_book(self, title: str) -> None:
        for book in self.books:
            if book.title == title and not book.is_borrowed:
                book.is_borrowed = True
                print(f"Book '{title}' has been borrowed. Enjoy Reading!")
                return
        print(f"Book '{title}' is not available for borrowing.")

    # Return a book
    def return_book(self, title: str) -> None:
        for book in self.books:
            if book.title == title and book.is_borrowed:
                book.is_borrowed = False
                print(f"Book '{title}' has been returned. Thank you!")
                return
        print(f"Book '{title}' was not borrowed from this library.")
#main code

def main():
    library = Library()
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. View Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")
        choice=input("Enter your choice (1-5): ")
        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            library.add_book(title,author)
        elif choice == "2":
            library.view_books()
        elif choice == "3":
            title = input("Enter the title of the book to borrow: ").strip()
            library.borrow_book(title)
        elif choice == "4":
            title = input("Enter the title of the book to return: ").strip()
            library.return_book(title)
        elif choice == "5":
            print("Exiting the Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main() 