from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix='/userdb', tags=['userdb'], responses={status.HTTP_404_NOT_FOUND: {'message': 'No encontrado'}})

users_list = []

# Get all users
# 127.0.0.1:8000/userdb
@router.get('/', response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())

# Get user by id
# 127.0.0.1:8000/userdb/64399702a537e76545eea435
@router.get('/{id}')
async def user(id: str):
    try:
        return search_user('_id', ObjectId(id))
    except:
        return {"User not found"}

# Get an user by id and name
# 127.0.0.1:8000/user/?id=1&name=user
@router.get('/')
async def user(id: str):
    return search_user('_id', id)

def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "User not found. Try localhost/user/?id=yourID&name=username"}

# Create user
# 127.0.0.1:8000/userdb
# JSON {"username": "user", "email": "example@example.com"}
@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user('email', user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already exists")
    users_list.append(user)
    user_dict = dict(user)
    del user_dict['id']
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({'_id': id}))
    return User(**new_user)

# User edit. The use of 'replace', in this case, modifies the whole user object
# instead of 'update', which modifies a specific field of user
# 127.0.0.1:8000/userdb
@router.put('/', response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict['id']

    try:
        found = db_client.local.users.find_one_and_replace({'_id': ObjectId(user.id)}, user_dict)

    except:
        return {'error': 'User not updated'}
    
    return search_user('_id', ObjectId(user.id))

# Deletes user
# 127.0.0.1:8000/userdb/64399702a537e76545eea435
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({'_id': ObjectId(id)})

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found to delete")
    else:
        return user