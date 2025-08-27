from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Product(BaseModel):
  id: int
  name: str
  price: float
  stock: int | None = None

class Seller(BaseModel):
  username: str
  full_name: str | None = None

@app.post("/product")
async def create_product(new_product: Product):
  return new_product

@app.post("/product")
async def create_product(new_product: Product):
  product_dict = new_product.model_dump()
  price_with_tax = new_product.price + (new_product.price * 18 / 100)
  product_dict.update({"price_with_tax": price_with_tax})
  return product_dict

@app.put("/products/{product_id}")
async def update_product(product_id: int, new_updated_product: Product, discount: float | None = None):
    return {"product_id": product_id, "new_updated_product": new_updated_product, "discount": discount}

@app.post("/product")
async def create_product(
  product: Product, 
  seller:Seller, 
  sec_key: Annotated[str, Body()]
  ):
  return {"product": product, "seller":seller, "sec_key":sec_key}


class Product(BaseModel):
    name: str = Field(examples=["Moto E"])
    price: float = Field(examples=[23.56])
    stock: int | None = Field(default=None, examples=[43])

@app.post("/products")
async def create_product(product: Product):
    return product


class Product(BaseModel):
  name: str
  price: float
  stock: int | None = None

  model_config = {
    "json_schema_extra": {
      "examples": [
        {
          "name": "Moto E",
          "price": 34.56,
          "stock": 45
        }
      ]
    }
  }

@app.post("/products")
async def create_product(product: Product):
    return product

