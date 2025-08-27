from fastapi import FastAPI, Cookie, Body, Header
from typing import Annotated, List, Any, Optional
from pydantic import BaseModel, Field

app = FastAPI()

@app.get('/products/recommendations')
async def get_recommendations(session_id: Annotated[str | None, Cookie()] = None):
  if session_id:
    return {"message": f"Recommendations for session {session_id}", "session_id": session_id}
  return {"message": "No session ID provided, showing default recommendations"}

class ProductCookies(BaseModel):
  session_id: str
  preferred_category: str | None = None
  tracking_id: str | None = None

@app.get("/products/recommendations")
async def get_recommendations(cookies: Annotated[ProductCookies, Cookie()]):
  response = {"session_id": cookies.session_id}
  if cookies.preferred_category:
    response["message"] = f"Recommendations for {cookies.preferred_category} products"
  else:
    response["message"] = f"Default recommendations for session {cookies.session_id}"
  if cookies.tracking_id:
      response["tracking_id"] = cookies.tracking_id
  return response

class ProductCookies(BaseModel):
  model_config = {"extra": "forbid"}
  session_id: str = Field(title="Session ID", description="User session identifier")
  preferred_category: str | None = Field(default=None, title="Preferred Category", description="User's preferred product category")

class PriceFilter(BaseModel):
    min_price: float = Field(ge=0, title="Minimum Price", description="Minimum price for recommendations")
    max_price: float | None = Field(default=None, title="Maximum Price", description="Maximum price for recommendations")

@app.post("/products/recommendations")
async def get_recommendations(
   cookies: Annotated[ProductCookies, Cookie()],
   price_filter: Annotated[PriceFilter, Body(embed=True)]
   ):
  response = {"session_id": cookies.session_id}
  if cookies.preferred_category:
    response["category"] = cookies.preferred_category
  response["price_range"] = {
        "min_price": price_filter.min_price,
        "max_price": price_filter.max_price
    }
  response["message"] = f"Recommendations for session {cookies.session_id} with price range {price_filter.min_price} to {price_filter.max_price or 'unlimited'}"
  return response 

class ProductHeaders(BaseModel):
  model_config = {"extra":"forbid"}
  authorization: str
  accept_language: str | None = None
  x_tracking_id: list[str] = []

@app.get("/products")
async def get_product(headers: Annotated[ProductHeaders, Header()]):
    return {
        "headers": headers
     }

class Product(BaseModel):
  id: int
  name: str
  price : float
  stock: int | None = None

class ProductOut(BaseModel):  
  name: str
  price : float

@app.get("/products/")
async def get_products() -> Product:
    return {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5}  

@app.get("/products/")
async def get_products() -> List[Product]:
    return [
       {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5},
       {"id": 2, "name": "Redmi 4", "price": 55.33, "stock": 7}
    ]

class BaseUser(BaseModel):
    username: str
    full_name: str | None = None

class UserIn(BaseUser):
    password: str

@app.post("/users/")
async def create_user(user: UserIn) -> BaseUser:
  return user

products_db = {
    "1": {"id": "1", "name": "Laptop", "price": 999.99, "stock": 10, "is_active": True},
    "2": {"id": "2", "name": "Smartphone", "price": 499.99, "stock": 50, "is_active": False}
}

class Product(BaseModel):
    id: str
    name: str
    price: float
    description: Optional[str] = None
    tax: float = 15.0


@app.get("/products/{product_id}", response_model=Product, response_model_include={"name", "price"})
async def get_product(product_id: str):
    return products_db.get(product_id, {})


@app.get("/products/{product_id}", response_model=Product, response_model_exclude={"tax", "description"})
async def get_product(product_id: str):
    return products_db.get(product_id, {})

