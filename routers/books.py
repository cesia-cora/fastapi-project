from fastapi import APIRouter, HTTPException, status
from db.models.book import Book
from db.schemas.book import book_schema, books_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"message": "Not found"}})

books_list = []

@router.get('/', response_model=list[Book])
async def books():
    return books_schema(db_client.local.books.find())

@router.get('/')
async def book(id: str):
    return search_book('_id', id)

def search_book(field: str, key):
    try:
        book = db_client.local.books.find_one({field: key})
        return Book(**book_schema(book))
    except:
        return {"error": "Book has not been found"}

@router.get('/{id}')
async def book(id: str):
    try:
        return search_book('_id', ObjectId(id))
    except:
        return {'Book has not been found'}

## Book Creation localhost:8000/books
## JSON {"title": "Otelo", "authors": "William Shakespeare", "isbn": 2304890294, "publisher": "L&PM Pocket", "language": "English", "number_of_pages": 300, "release": "20/09/1996"}
@router.post('/', response_model=Book, status_code=status.HTTP_201_CREATED)
async def book(book: Book):
    if type(search_book('isbn', book.isbn)) == Book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book already exists")
    books_list.append(book)
    book_dict = dict(book)
    del book_dict['id']
    id = db_client.local.books.insert_one(book_dict).inserted_id
    new_book = book_schema(db_client.local.books.find_one({'_id': id}))
    return Book(**new_book)

# Update book fields localhost:8000/books
# JSON {"id": "646398956d13bdaa899a0b68", "title": "Otelo", "authors": "William Shakespeare", "isbn": 2304890295, "publisher": "L&PM Pocket", "language": "English", "number_of_pages": 500, "release": "20/09/1996"}
@router.put('/', response_model=Book)
async def book(book: Book):
    book_dict = dict(book)
    del book_dict['id']

    try:
        found = db_client.local.books.find_one_and_replace({'_id': ObjectId(book.id)}, book_dict)

    except:
        return {'error': 'Book not updated'}
    
    return search_book('_id', ObjectId(book.id))

# Delete book localhost:8000/books/646398956d13bdaa899a0b68
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def book(id: str):
    found = db_client.local.users.find_one_and_delete({'_id': ObjectId(id)})

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found to delete")
    else:
        return book