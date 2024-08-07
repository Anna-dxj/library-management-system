# Libarary Book Management System

Create a simple library book management system using Python. The system should allow users to add books, search for books, and display the library inventory. Use both lists and dictionaries in your implementnation. 

## Requirements
1. Create a dictionary called `library` to store book information
    - Keys should be book IDs (integer)
    - Values should be dictionaries containinng book details (title, author, quantity)
2. Implement the following functions:
    - `add_book(book_id, title, author, quantity)`: adds a new book to the library or update the quantity if book already exists
    - `remove_book(book_id)`: Remove a book from the library by its ID
    - `search_book(keyword)`: search for books by the title or author, returning a list of matching book IDs
    - `display_inventory()`: display the entire library, sorted by ID
3. Add the following functionality to using lists
    - Maintain a list called `borrowed_books` to keep track of borrowed books. Each entry in the list should be a dictionary containing book ID, borrower name, and borrow date 
    - Implement a function `borrow_book(book_id, borrower_name, borrow_date)` to add an entry to the `borrowed_books` list and decrease the quantity of the book in the library 
    - Implement a function `return_book(book_id)` to remove an entry from the `borrowed_books` list and increase the quantity of the book in the library 
4. Use appropriate lists and dictionary methods in your emplementation (eg., `append()`, `remove()`, `key()`, `values()`, `items()`)
5. Implement error handling for cases such as trying to remove a non-existent book, borrowing a book that is out of stock, or adding a book with an existing ID
6. Create a simple menu-driven interface that allows users to interact with the library sistem