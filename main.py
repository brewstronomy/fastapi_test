from fastapi import FastAPI, security, responses, Depends
from typing import Annotated

path_img = "./img/"  # path relative to main.py

app = FastAPI()

# root page
@app.get("/")
async def root():
    return {"message": "Hello World!"}

# testing variable endpoints and file responses
@app.get("/{cat}")
async def cat_endpoint(cat: str):  # enforcing str input
    return responses.FileResponse(path_img + f"{cat}.jpg")

# basic OAuth2 authorization -- using Bearer token
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):  # Annotated part means token is expected to be a string, with metadata specifying that it depends on the authorization scheme
    return {"token": token}