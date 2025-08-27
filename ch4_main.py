from fastapi import FastAPI, Query, Path
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()

PRODUCTS = [
    {"id": 1, "title": "Ravan Backpack", "price": 109.95, "description": "Perfect for everyday use and forest walks."},
    {"id": 2, "title": "Slim Fit T-Shirts", "price": 22.3, "description": "Comfortable, slim-fitting casual shirts."},
    {"id": 3, "title": "Cotton Jacket", "price": 55.99, "description": "Great for outdoor activities and gifting."},
]


@app.get("/products")
async def get_products(search: Annotated[str | None, Query(min_length=3)] = None):
  if search:
    search_lower = search.lower()
    filtered_products = []
    for product in PRODUCTS:
      if search_lower in product["title"].lower(): 
        filtered_products.append(product)
    return filtered_products
  return PRODUCTS 


@app.get("/products")
async def get_products(search: Annotated[list[str] | None, Query()] = None):
  if search:
    filtered_products = []
    for product in PRODUCTS:
      for s in search:
        if s.lower() in product["title"].lower():
          filtered_products.append(product)
    return filtered_products
  return PRODUCTS

@app.get("/products/")
async def get_products(search: Annotated[
        str | None,
        Query(title="Search Products", description="Search by Product Title")
    ] = None
    ):
    if search:
        search_lower = search.lower()
        filtered_products = []
        for product in PRODUCTS:
            if search_lower in product["title"].lower():
                filtered_products.append(product)
        return filtered_products
    return PRODUCTS

def check_valid_id(id: str):
  if not id.startswith("prod-"):
    raise ValueError("ID must start with 'prod-'")
  return id

@app.get("/products/")
async def get_products(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        return {"id": id, "message": "Valid product ID"}
    return {"message": "No ID provided"}

@app.get('/product/{product_id}')
async def get_product(product_id: Annotated[int, Path(ge=1, le=3)]):
    for product in PRODUCTS:
        if product['id'] == product_id:
            return product
    return {'error': 'Product not found'}


@app.get("/products/{product_id}")
async def get_product(
    product_id: Annotated[int, Path(gt=0, le=100)],
    search: Annotated[str | None, Query(max_length=20)] = None
):
    for product in PRODUCTS:
        if product["id"] == product_id:
            if search and search.lower() not in product["title"].lower():
                return {"error": "Product does not match search term"}
            return product
    return {"error": "Product not found"}

