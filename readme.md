# FastAPI Project

<hr>

### Overview:
Book API created with Python and MondoDB.

### Features:
* CRUD method
* User authentication
* Search and pagination

### Command to run:

`py -m uvicorn main:app --reload`

### Routes:

`localhost:8000/books`

Book creation JSON example
<br>`{"title": "Otelo", "authors": "William Shakespeare", "isbn": 2304890294, "publisher": "L&PM Pocket", "language": "English", "number_of_pages": 300, "release": "20/09/1996"}`

Book upgrade JSON example
<br>`{"id": "646398956d13bdaa899a0b68", "title": "Otelo", "authors": "William Shakespeare", "isbn": 2304890295, "publisher": "L&PM Pocket", "language": "English", "number_of_pages": 500, "release": "20/09/1996"}`

Book deletion
<br>`localhost:8000/books/646398956d13bdaa899a0b68`