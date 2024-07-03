def is_author(book, current_user):
    """
    Mehthod that checks if authenticated user is the author of the book.

    """
    return book.author == current_user
