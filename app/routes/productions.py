from fastapi import APIRouter
from app.database import production_collection
from app.models.productions import Production
import datetime
from datetime import UTC

production_router = APIRouter()

@production_router.post("/production")
async def add_production(production: Production):



    production_dict = production.model_dump()
    production_dict["date"] = datetime.datetime.now(UTC)
    new_production = await production_collection.insert_one(production_dict)
    return {"message": "Production recorded", "production_id": str(new_production.inserted_id)}


@production_router.get("/production")
async def get_production():
    production = await production_collection.find().to_list(100)
    return production


