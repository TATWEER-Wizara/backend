#crud for inventory
from fastapi import APIRouter, HTTPException
from app.models.inventory import Inventory
from app.database import inventory_collection
from bson import ObjectId
from datetime import datetime


inventory_router = APIRouter()

@inventory_router.post("/inventory", response_model=Inventory)
async def create_inventory(inventory: Inventory):
    inventory_dict = inventory.model_dump()
    inventory_dict["created_at"] = datetime.now(datetime.UTC)

    new_inventory = await inventory_collection.insert_one(inventory_dict)
    return Inventory(**inventory_dict, id=str(new_inventory.inserted_id))


@inventory_router.get("/inventory/{inventory_id}", response_model=Inventory)
async def get_inventory(inventory_id: str):
    inventory = await inventory_collection.find_one({"_id": ObjectId(inventory_id)})

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return Inventory(**inventory)


@inventory_router.put("/inventory/{inventory_id}", response_model=Inventory)
async def update_inventory(inventory_id: str, inventory: Inventory):
    inventory_dict = inventory.model_dump()

    inventory_dict["updated_at"] = datetime.now(datetime.UTC)
    await inventory_collection.update_one({"_id": ObjectId(inventory_id)}, {"$set": inventory_dict})
    return Inventory(**inventory_dict, id=str(inventory_id))


@inventory_router.delete("/inventory/{inventory_id}", response_model=Inventory)
async def delete_inventory(inventory_id: str):
    inventory = await inventory_collection.find_one({"_id": ObjectId(inventory_id)})

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    await inventory_collection.delete_one({"_id": ObjectId(inventory_id)})
    return Inventory(**inventory)


@inventory_router.get("/inventory", response_model=list[Inventory])
async def get_inventory_list():
    inventory = await inventory_collection.find().to_list(100)

    return [Inventory(**inventory) for inventory in inventory]






