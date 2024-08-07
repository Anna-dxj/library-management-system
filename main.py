# Import date time to be able to automatically generate current date
from datetime import datetime

# Initiate `library` dictionary and `borrowed_books` list
library = {}
borrowed_books = []

def check_book_id(id, mode):
    '''Converts `id` to an integer & checks if the ID based on its purpose meets the criteria'''
    try:
        # Checks if `id` is an integer and raises error if not
        if not id.isdigit():
            raise ValueError('Book ID must be a non-negative integer')

        int_id = int(id)

        if mode == 'access':
            # If trying to access a pre-existing `id`, checks to see if it exists in library
            # If not in library, raises error
            if int_id not in library:
                raise KeyError('Book is not in library. Please confirm ID.')
        elif mode == 'create':
            # If trying to create a new `id`, checks if it is a non-negative number
            # If it is, raises error
            if int_id < 0:
                raise ValueError('Book ID must be a non-negative integer.')
            
            # Checks if id already exists and raises error if so
            if int_id in library: 
                raise ValueError('Book ID already exists!')
        elif mode == 'borrow':
            # If trying to borrow book by `id`, first checks if book is in library
            if int_id not in library:
                raise KeyError('Book is not in library. Please confirm ID.')
            
            # Checks if all target books in library are checked out. If so, raises error
            if library[int_id]['quantity'] == 0:
                raise ValueError('Book is out of stock. Please try again later')
        elif mode == 'return':
            # If trying to return borrow book by `id`, first checks if book is in library
            if int_id not in library:
                raise KeyError('Book is not in library. Please confirm ID.')
            
            # Initiates switch
            is_borrowed = False

            # Loops through book items in `borrowed_book` list
            for book in borrowed_books:
                # Checks if target `book` is checked out and sets the switch to true & breaks loop if true
                if int_id == book['book id']:
                    is_borrowed = True
                    break
            
            # If loop did not find a match, book is not checked out and raises an error
            if is_borrowed == False:
                raise KeyError('The book you wish to return is not checked out! Please confirm book ID.')

        return int_id
    except ValueError as e:
        print(e)
        menu()
    except KeyError as e:
        print(e)
        menu()

def check_quantity(num, mode=None):
    '''Converts quantity `num` to an integer and applies checcks to ensure it is a valid input. Returns `num` as an integer.'''
    try:
        if mode == 'update' and num == '':
            return 0

        if not num.isdigit():
            raise ValueError('Quantity must be a non-negative integer')
        
        quantity_int = int(num)

        if quantity_int < 0:
            raise ValueError('Quantity must be a non-negative integer')
        
        return quantity_int
    except ValueError as e:
        print(e)
        menu()

def check_menu(num):
    '''Checks valid menu input and returns as integer'''

    try:
        # Checks if `num` is a non-integer
        if not num.isdigit():
            raise ValueError('Please enter a number 1~8')
        
        int_num = int(num)

        # Checks if `int_num` is outside range of menu options
        if int_num > 8 or int_num < 0:
            raise ValueError('Please enter a number 1~8')
        
        return int_num
    except ValueError as e:
        print(e)
        menu()
        
def check_string(str):
    '''Checks if string is empty. Returns string if not'''
    try:
        if not str:
            raise ValueError('\nTitle and author cannot be left empty')
        
        return str
    except ValueError as e:
        print(e)
        menu()

def add_book(book_id, quantity, title=None, author=None): 
    '''Adds a new book to the library dictionary or updates the book information if it already exists'''
    
    # Checks if book exists
    if library.get(book_id):
        # Updates the book information, with user input
        print('Updating book...\n')
        library[book_id]['quantity'] += quantity
        if title:
            library[book_id]['title'] = title
        
        if author:
            library[book_id]['author'] = author
        
        print(f'{library[book_id]['title']} has been updated.')
    else: 
        # Add book to library
        print('\nAdding book...')
        library[book_id] = {
            'title': title,
            'author': author,
            'quantity': quantity
        }
        print(f'\n{title} has been added to the library.')

def remove_book(book_id):
    '''Removes a book from the library dictionary by its ID'''

    # Uses book_id from library to target and remove that item from `library` dictionary
    removed_book = library.pop(book_id)
    print(f'Removing book...\n\n{removed_book['title']} has been removed from the library.')


def search_book(keyword):
    '''Searches for a book in library dictionary by title or author keyword (user input) and returns a list of matching book IDs'''
    print('\nSearching for book...\n')

    # Creates a list of `book_id`s that that correspond to books that contain the `keyword` as a substring in either the `title` or `author`
    book_list = [book_id for (book_id, book) in library.items() if keyword in book['author'].lower() or keyword in book['title'].lower()]

    # Checks if `keyword` would return an empty list
    if len(book_list) == 0:
        print('No book contains that keyword')
    else: 
        print(f'List of book IDs that match your search:\n{book_list}')

def display_inventory():
    '''Displasy the entire library inventory, sorted by book ID'''

    # Checks if `library` has any items
    if library:
        print(f'\nHere is a list of all books in the library:\n')
        # If library is not empty, sorts dictionary by keys
        sorted_library = dict(sorted(library.items()))

        for book_id in sorted_library:
            title = library[book_id]['title']
            author = library[book_id]['author']
            quantity = library[book_id]['quantity']
            print(f'{book_id}: {title} - {author} (amount: {quantity})')
    else:
        print('The library is empty. Please add books first.')

def borrow_books(book_id, borrower_name, borrow_date): 
    '''Adds an entry to the `borrowed_books` list and decreaes the quantity of the book in the library'''
    # Formats date input into YYYY-MM-DD format
    formatted_date = borrow_date.strftime('%Y-%m-%d')

    # Creates a dictionary representing a borrowed book
    book = {
        'book id': book_id, 
        'borrower name': borrower_name,
        'borrow date': formatted_date
    }

    # Adds book to the `borrowed_book` list
    borrowed_books.append(book)

    # Removes a copy from library
    library[book_id]['quantity'] -= 1

    print(f'\n You have borrowed {library[book_id]['title']}')
   

def return_book(book_id):
    '''Removes an entry from the `borrowed_books` list and increases the quantity of the book in the library''' 
    try:
        name = input('Enter your name: ').strip().lower()
        
        # Sets a flag for if book is found or not
        is_found = False

        for book in borrowed_books: 
            # If a user has both checkcked out a book and that book is checked out, confirms that the user was the one who checked out the book initially
            if book['book id'] == book_id and book['borrower name'].lower() == name:
                target_book = book
                is_found = True
                break

        # Raises error if after looping through all books, book is not found
        if not is_found:
            raise ValueError('You cannot return a book you have not checked out or a book with the incorrect ID.')
    except KeyError as e: 
        print(e)
        menu()
    except ValueError as e:
        print(e)
        menu()
    else:
        # Gets the index of the target dictionary
        index = borrowed_books.index(target_book)

        # Removes target dictionary from the array of `borrowed_books`
        borrowed_books.pop(index)

        # Increases the number of copies of that book in `library` dictionary
        library[book_id]['quantity'] += 1

        print(f'\nYou have returned {library[book_id]['title']}')

def menu():
    # Menu options
    print('\n1. Add a book to the library')
    print('2. Update a book in the library')
    print('3. Remove a book from the library')
    print('4. Search for a book')
    print('5. Display current inventory')
    print('6. Borrow a book')
    print('7. Return a book')
    print('8. Exit\n')

    user_choice_input = input('Please choose what you would like to do (1~8):\n').strip()

    user_choice = check_menu(user_choice_input)

    # Add a book to the library:
    if user_choice == 1: 
        print('\nTo add a book to the library, please enter the following:\n')

        book_id_input = input('Enter book ID (numbers only): ').strip()

        # Converts `book_id_input` into integer and ensures valid input
        book_id = check_book_id(book_id_input, 'create')
                
        quantity_input = input('How many quantities are you adding to the library? ').strip()
                
        # Converts `quantity_input` into integer and ensures valid input
        quantity = check_quantity(quantity_input)                

        title_input = input('Enter the title of the book: ').strip().title()

        # Checks validity of `title_input`
        title = check_string(title_input)

        author_input = input('Enter the author of the book: ').strip().title()

        # Checks validity of `author_input`
        author = check_string(author_input)

        add_book(book_id=book_id, quantity=quantity, title=title, author=author)

        # Returns to menu
        menu()
    # Updates existing book
    elif user_choice == 2:
        print('\nTo update a book to the library, please enter the following: \n')
        book_id_input = input('Enter book ID: ').strip()

        # Converts `book_id_input` into integer & ensures valid input
        book_id = check_book_id(book_id_input, 'access')

        quantity_input = input('How many quantities are you adding to the library? If you do not wish to add more copies, leave this empty. ').strip()

        # Converts `quantity_input` into integer & ensures valid input
        quantity = check_quantity(quantity_input, 'update')
                
        # Provides the option for a user only update the quantity of books in library and the option to update a book's information in the events of typos
        title = input('Enter the title of the book. If you do not wish to update the title, leave this empty: ').strip().title()
        author = input('Enter the author of the book. If you do not wish to update the author, leave this empty: ').strip().title()

        add_book(book_id=book_id, quantity=quantity, title=title, author=author)

        # Returns to menu
        menu()
    # Remove book from library
    elif user_choice == 3: 
        print('\nTo remove a book from the library, please enter the following: \n')
        book_id_input = input('Enter book ID: ').strip()

        # Converts `book_id_input` into integer and & ensures valid input
        book_id = check_book_id(book_id_input, 'access')

        remove_book(book_id)

        # Returns to menu
        menu()
    # Return a list of `book_id`s from a keyword search
    elif user_choice == 4: 
        print('\nSearching for a book by author or book title: \n')
        # `keyword` corresponds to a substring that can be in either a book title or author, so there are less checks on `keyword` input
        keyword = input('Keyword: ').strip().lower()
        search_book(keyword)
        menu()
    # Display whole library
    elif user_choice == 5: 
        display_inventory()
        menu()
    # Check out book
    elif user_choice == 6: 
        print('\nTo borrow a book, please enter the following: ')
        # Asks for borrower name
        borrower_name = input('Your name: ').title().strip()
        book_id_input = input('Book ID of the book you wish to borrow: ').strip()

        # Converts `book_id_input` to an integer & insures input is valid
        book_id = check_book_id(book_id_input, 'borrow')

        # Automatically gets the current date
        now = datetime.now()
        borrow_date = now.date()

        borrow_books(book_id=book_id, borrower_name=borrower_name, borrow_date=borrow_date)

        # Returns to menu after success
        menu()
    # Return book
    elif user_choice == 7:
        # If no books are checked out, prevents a user from returning a book
        if len(borrowed_books) == 0:
            print('\nThere are no books checked out!')
            menu()

        print('\nTo return a book, please enter the following: ')
            
        book_id_input = input('Book ID of the book you wish to return: ').strip()

        # Converts `book_id_input` to an integer & insures input is valid
        book_id = check_book_id(book_id_input, 'return')

        return_book(book_id)

        # Returns to menu after success
        menu()
    # Exits program
    elif user_choice == 8:
        print('\nExiting the program...')
        return

def main():
    print('Welcome to the Library Book Management system!')
    menu()

main()