def book_schema(book) -> dict:
    return {'id': str(book['_id']),
            'title': book['title'],
            'authors': book['authors'],
            'isbn': book['isbn'],
            'publisher': book['publisher'],
            'language': book['language'],
            'number_of_pages': book['number_of_pages'],
            'release': book['release'],
            'image_url': book['image_url']}

def books_schema(books) -> list:
    return [book_schema(book) for book in books]