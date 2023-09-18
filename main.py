from fastapi import FastAPI, security, responses, Depends, HTTPException, status
from typing import Annotated, Union
from pydantic import BaseModel

path_img = "./img/"  # path relative to main.py

app = FastAPI()

# initializing Authorization scheme (using Bearer Tokens)
# tokenUrl parameter defines a relative path where tokens will be generated -- i.e. if host is example.com, tokens will be generated at the url example.com/token
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")

# creating a user model
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[str, None] = None

# building a fake user database for authorization testing
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "awonderson@test.org",
        "hashed_password": "fakehashedsecret2",
        "disabled": True
    }
}

# Pydantic model that extends User to include a string-valued hashed password
class UserInDB(User):
    hashed_password: str

# dependency for pulling user info from a database given the username
def get_user(db, username: str):
    if username in db:  # checking if user exists
        user_dict = db[username]
    return UserInDB(**user_dict)

# fake function for decoding tokens
def fake_decode_token(token):
    # no functionality
    user = get_user(fake_users_db, token)
    return user

# fake function for hashing passwords
def fake_hashed_password(password: str):
    return "fakehashed" + password

# dependency for pulling current user (and checking its credentials)
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)  # right now, this pulls the User instance from the fake db
    # check if token corresponds to a valid user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})  # this line follows HTTP 401 specs -- can be skipped but obeys compliance with specs
    return user

# dependency for only pulling a user that's active (depends on get_current_user, which itself uses get_user)
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="inactive user")
    return current_user

# root page
@app.get("/")
async def root():
    return {"message": "Hello World!"}

# testing variable endpoints and file responses
@app.get("/{cat}")
async def cat_endpoint(cat: str):  # enforcing str input
    return responses.FileResponse(path_img + f"{cat}.jpg")

# path operation for logging in
@app.post("/token")
async def login(form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()]):
    # argument is equivalent to writing >form_data: Annotated[security.OAuth2PasswordRequestForm, Depends(security.OAuth2PasswordRequestForm)]
    # this is because the OAuth2... dependency is itself the class that will be called to create the form_data instance
    user_dict = fake_users_db.get(form_data.username)  # pull user info from form_data username
    if not user_dict:  # triggers if form_data.username doesn't correspond to a known user
        raise HTTPException(status_code=400, detail="incorrect username or password")
    user = UserInDB(**user_dict)  # assuming user exists, initialize its User model
    hashed_password = fake_hash_password(form_data.password)  # hash the password from form_data
    if not hashed_password == user.hashed_password:  # compare form_data hashed password to user's stored hashed password
        raise HTTPException(status_code=400, detail="incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


# define a get user path operation
@app.get("/users/me"):
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user