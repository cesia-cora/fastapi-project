from fastapi import FastAPI, Request
from routers import books, users_db
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db.schemas.book import books_schema
from db.client import db_client

app = FastAPI()

# py -m uvicorn main:app --reload

app.include_router(books.router)
app.include_router(users_db.router)
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
def all_books(request: Request, page: int = 1, page_size: int = 10):
    books_query = db_client.local.books.find()
    total_books = db_client.local.books.count_documents({})
    total_pages = (total_books + page_size - 1) // page_size
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_books = books_query[start_index:end_index]
    result = books_schema(paginated_books)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'books_list': result,
        'total_pages': total_pages,
        'page': page
    })

""" @app.get('/search', response_class=HTMLResponse)
def search_books(request: Request, term: str, page: int = 1, page_size: int = 10):
    books_query = db_client.local.books.find({'title': {'$regex': term, '$options': 'i'}}) if term else db_client.local.books.find()
    total_books = books_query.count()
    total_pages = (total_books + page_size - 1) // page_size
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_books = books_query[start_index:end_index]
    result = books_schema(paginated_books)
    return templates.TemplateResponse('search.html', {
        'request': request,
        'term': term,
        'books_list': result,
        'total_pages': total_pages,
        'page': page
    }) """