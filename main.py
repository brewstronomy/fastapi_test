from fastapi import FastAPI, security, responses, Depends
from typing import Annotated, Union
from pydantic import BaseModel

path_img = "./img/"  # path relative to main.py

app = FastAPI()

# basic OAuth2 authorization -- using Bearer token
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")  # frontend sends credentials to API, and stores the resulting token
# tokenUrl parameter defines a relative path where the token info will be stored -- e.g. if API is at test.com, the tokenURL would be test.com/token
# but that path is not CREATED, just 'reserved'

# creating a Pydantic user model 
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[str, None] = None

# root page
@app.get("/")
async def root():
    return {"message": "Hello World!"}

# testing variable endpoints and file responses
@app.get("/{cat}")
async def cat_endpoint(cat: str):  # enforcing str input
    return responses.FileResponse(path_img + f"{cat}.jpg")

# (fake) path operation for reading items
@app.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):  # Annotated part means token is expected to be a string, with metadata specifying that it depends on the authorization scheme
    return {"token": token}  # the token input is because this action requires authentication -- for authentication, front end sends an Authorization header (including "Bearer" and the token value)


# (fake) utility function for decoding usernames
def fake_decode_token(token):
    return User(username=token + "fakedecoded",
                email="fakeemail@example.com",
                full_name="Fakey McFakerton")

# dependency for pulling usernames (depends on authorization scheme)
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

# define a get user path operation
@app.get("/users/me"):
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user