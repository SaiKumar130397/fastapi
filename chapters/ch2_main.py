from fastapi import FastAPI 
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class NumberRequest(BaseModel):
    num: int
    char: str = 'cube'

class arrayRequest(BaseModel):
    arr: list[int]

@app.get('/')
def home():
    return {'message': 'Hello Fast API'}

@app.get('/abcd')
def abcd():
    return {'message': 'Started Fast API'}

@app.post('/cube')
async def a(request: NumberRequest):
    return {request.char: request.num**3}

@app.post('/sum')
async def b(request: arrayRequest):
    return {'sum': sum(request.arr)}     

@app.get('/item/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id,}

@app.post('/item')
async def create_item(new_item: dict):
    return {'new_item': new_item}

@app.put('/item/{item_id}')
async def update_item(updated_item: dict, item_id: int):
    return {'updated_item': updated_item} 

@app.patch('/item/{item_id}')   
async def partial(updated_item: dict, item_id: int):
    return {'updated_item': updated_item} 

@app.delete('/item/{item_id}')
async def delete_item(item_id: int):
    return {'item_id': item_id}

class productcategory(str, Enum):
    books ="books"
    pens = "pens"
    pencil = "pencil" 

@app.get('/product/{category}')
async def get_product(category: productcategory):
    if category == productcategory.books:
        return {'category': category, 'message': 'Great book!!'}
    elif category.value == 'pencil':
        return {'category': category, 'message': 'Nice pencil!'}
    else:
        return {'category': category, 'message': 'Smooth pen!'}

@app.get("/product")
async def product(category:str, limit:int):
  return {"status":"OK", "category":category, "limit":limit}

@app.get("/product/{year}")
async def product(year:str, category:str):
  return {"status":"OK", "year":year, "category":category}
