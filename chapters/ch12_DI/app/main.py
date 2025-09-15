from fastapi import FastAPI, Depends, Header, HTTPException 
from typing import Annotated 

app = FastAPI()

# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#   return {"q": q, "skip": skip, "limit": limit}

# @app.get("/items")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
#   return commons

# @app.get("/users")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
#   return commons 

# CommonsDep = Annotated[dict, Depends(common_parameters)]

# @app.get("/products")
# async def read_products(commons: CommonsDep):
#   return commons

# @app.get("/carts")
# async def read_carts(commons: CommonsDep):
#   return commons

# class CommonQueryParams:
#   def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
#     self.q = q
#     self.skip = skip
#     self.limit = limit


# @app.get("/items")
# async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
#   return commons

# @app.get("/users")
# async def read_users(commons: Annotated[CommonQueryParams, Depends()]):
#   return commons

# CommonsDep = Annotated[CommonQueryParams, Depends(CommonQueryParams)]

# @app.get("/products")
# async def read_products(commons: CommonsDep):
#   return commons

# @app.get("/carts")
# async def read_carts(commons: CommonsDep):
#   return commons

# async def verify_token(x_token: Annotated[str, Header()]):
#   if x_token != "130397":
#     raise HTTPException (status_code=400, detail="X-Token header invalid")
  
# @app.get("/items", dependencies=[Depends(verify_token)])
# async def read_items():
#   return {"data": "All Items"}

# #Global Dependecies
# async def verify_token(x_token: Annotated[str, Header()]):
#   if x_token != "130397":
#     raise HTTPException (status_code=400, detail="X-Token header invalid")

# app = FastAPI(dependencies=[Depends(verify_token)])

# @app.get("/items")
# async def read_items():
#     return {"data": "All Items"}

# @app.get("/products")
# async def read_products():
#     return {"data": "All Products"}

# Dependencies with yield
class OwnerError(Exception):
  pass

def get_username():
  try:
    yield "Sai"
  except OwnerError as e:
    raise HTTPException(status_code=400, detail=f"Owner error: {e}")
  
@app.get("/items/{item_id}")  
def get_items(item_id: str, username: Annotated[str, Depends(get_username)]):
    data = {
    "pressure-cooker": 
      {"description": "Essential for making dal-chawal", 
       "owner": "Kumar" },
    "scooty": 
      {"description": "Zippy ride for city streets", 
       "owner": "Sai" },
    }

    if item_id not in data:
      raise HTTPException(status_code=404, detail="Item not found")
    
    item = data[item_id]

    if item["owner"] != username :
      raise OwnerError(username)
    
    return item 