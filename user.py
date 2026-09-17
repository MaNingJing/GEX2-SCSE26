## This module contains the user interface for the library system.
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module.
from admin import (
    load_library,
    save_library,
    find_book
)


## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    if category is None:
        return []

    target = category.strip().lower()

    if target == "":
        return []

    result = []

    for book_id, book in books.items():
        if book["category"].lower() == target:
            result.append(book_id)

    return result


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    if search_text is None:
        return []

    target = search_text.strip().lower()

    if target == "":
        return []

    result = []

    for book_id, book in books.items():
        if target in book["title"].lower():
            result.append(book_id)

    return result


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None:
        return "EMPTY_NAME"

    cleaned_borrower = borrower.strip()

    if cleaned_borrower == "":
        return "EMPTY_NAME"

    book = books[book_id]

    if not book["available"]:
        return "NOT_AVAILABLE"

    book["available"] = False

    loans.append({
        "book_id": book_id,
        "borrower": cleaned_borrower
    })

    return "OK"


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"
def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None:
        return "EMPTY_NAME"

    cleaned_borrower = borrower.strip()

    if cleaned_borrower == "":
        return "EMPTY_NAME"

    if books[book_id]["available"]:
        return "NOT_ON_LOAN"

    loan_index = -1

    for i, loan in enumerate(loans):
        if loan["book_id"] == book_id:
            loan_index = i
            break

    if loan_index == -1:
        return "NOT_ON_LOAN"

    loans.pop(loan_index)

    books[book_id]["available"] = True

    return "OK"


## The main function that runs the user interface for the library system.
def main():
    data = load_library("library.json")

    if data is None:
        return

    books = data["books"]
    loans = data["loans"]

    while True:
        print()
        print("LIBRARY USER SYSTEM")
        print("=" * 60)
        print("1. Search books by category")
        print("2. Search books by title")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        print("=" * 60)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            category = input("Enter category: ").strip()
            result = books_in_category(books, category)

            if len(result) == 0:
                print("No books found in this category.")
            else:
                print(f"Found {len(result)} book(s):")
                for book_id in result:
                    book = books[book_id]
                    print(f"  {book_id} | {book['title']}")

        elif choice == "2":
            search_text = input("Enter title (or part of title): ").strip()
            result = search_by_title(books, search_text)

            if len(result) == 0:
                print("No books found matching this title.")
            else:
                print(f"Found {len(result)} book(s):")
                for book_id in result:
                    book = books[book_id]
                    print(f"  {book_id} | {book['title']}")

        elif choice == "3":
            search_text = input("Enter book ID, title, or author: ").strip()
            borrower = input("Enter your name: ").strip()

            result = borrow_book(books, loans, search_text, borrower)

            if result == "OK":
                print("Book borrowed successfully!")
            elif result == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif result == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif result == "NOT_AVAILABLE":
                print("Error: Book is not available (already on loan).")

        elif choice == "4":
            book_title = input("Enter book ID, title, or author: ").strip()
            borrower = input("Enter your name: ").strip()

            result = return_book(books, loans, book_title, borrower)

            if result == "OK":
                print("Book returned successfully!")
            elif result == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif result == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif result == "NOT_ON_LOAN":
                print("Error: Book is not currently on loan.")

        elif choice == "5":
            save_library(data, "library.json")
            print("Library data saved. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()