from fastapi import APIRouter, Depends
from app.database import sales_collection
from app.models.sales import Sale
from bson import ObjectId
import datetime


sales_router = APIRouter()

@sales_router.post("/sales")
async def add_sale(sale: Sale):

    sale_dict = sale.model_dump()
    sale_dict["date"] = datetime.datetime.now(datetime.UTC)
    new_sale = await sales_collection.insert_one(sale_dict)
    return {"message": "Sale recorded", "sale_id": str(new_sale.inserted_id)}

@sales_router.get("/sales")
async def get_sales():
    sales = await sales_collection.find().to_list(100)

    return sales
