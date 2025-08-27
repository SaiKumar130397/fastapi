from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Annotated
from pydantic import BaseModel, Field
import os
import uuid
import shutil

app = FastAPI() 

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <body>
            <h2>Login Form</h2>
            <form action="/login/" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username"><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "password_length": len(password)}

class FormData(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3, max_length=20) 

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
        <body>
            <h2>Single File Upload (bytes)</h2>
            <form action="/files/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
            <h2>Single File Upload (UploadFile)</h2>
            <form action="/uploadfile/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """

@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    
    filename = f"{uuid.uuid4()}.bin"
    save_path = f"uploads/{filename}"

    os.makedirs("uploads", exist_ok=True)

    with open(save_path, "wb") as buffer:
        buffer.write(file)

    return {"file size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: Annotated[UploadFile | None, File()] = None):
    if not file:
        return {"message": "No upload file sent"}
    
    save_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "content_type": file.content_type} 

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
        <body>
            <h2>Multiple Files Upload (UploadFile)</h2>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """

@app.post("/uploadfiles/")
async def create_upload_file(files: Annotated[list[UploadFile], File()]):
    save_files = []
    os.makedirs("uploads", exist_ok=True)
    for file in files:
        save_path = f"uploads/{file.filename}"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        save_files.append({"filename": file.filename})
    return save_files 

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <head>
            <title>User Profile Upload</title>
        </head>
        <body>
            <h2>User Profile Form</h2>
            <form action="/user-with-file/" enctype="multipart/form-data" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br><br>
                <label for="file">Profile Picture (optional):</label><br>
                <input type="file" id="file" name="file" accept="image/*"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """
@app.post("/user-with-file/")
async def create_user_with_file(
    username: Annotated[str, Form()],
    file: Annotated[UploadFile | None, File()] = None
):
    response = {"username": username}
    if file:
        save_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        response["filename"] = file.filename
    return response

items = {
  "apple": "A juicy fruit", 
  "banana": "A yellow delight"
  }

@app.get("/items/{item_id}")
async def read_item(item_id: str):
  if item_id not in items:
    raise HTTPException(status_code=404, detail="Item not found")
  return items[item_id]