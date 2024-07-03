def serialize_book(book):
    """JSON serialized data for a book object"""
    return {
        "id": book.id,
        "title": book.title,
        "published_date": book.published_date,
        "author": {
            "id": book.author.id,
            "username": book.author.username,
            "email": book.author.email,
        },
    }
