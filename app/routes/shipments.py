#crud for shipments

from fastapi import APIRouter, HTTPException
from app.models.shipments import Shipment
from app.database import shipments_collection
from bson import ObjectId
from datetime import datetime


shipments_router = APIRouter()

@shipments_router.post("/shipments", response_model=Shipment)
async def create_shipment(shipment: Shipment):
    shipment_dict = shipment.model_dump()
    shipment_dict["created_at"] = datetime.now(datetime.UTC)

    new_shipment = await shipments_collection.insert_one(shipment_dict)
    return Shipment(**shipment_dict, id=str(new_shipment.inserted_id))


@shipments_router.get("/shipments/{shipment_id}", response_model=Shipment)
async def get_shipment(shipment_id: str):
    shipment = await shipments_collection.find_one({"_id": ObjectId(shipment_id)})

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return Shipment(**shipment)


@shipments_router.put("/shipments/{shipment_id}", response_model=Shipment)
async def update_shipment(shipment_id: str, shipment: Shipment):
    shipment_dict = shipment.model_dump()
    shipment_dict["updated_at"] = datetime.now(datetime.UTC)

    await shipments_collection.update_one({"_id": ObjectId(shipment_id)}, {"$set": shipment_dict})
    return Shipment(**shipment_dict, id=str(shipment_id))


@shipments_router.delete("/shipments/{shipment_id}", response_model=Shipment)
async def delete_shipment(shipment_id: str):
    shipment = await shipments_collection.find_one({"_id": ObjectId(shipment_id)})

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    await shipments_collection.delete_one({"_id": ObjectId(shipment_id)})
    return Shipment(**shipment)


@shipments_router.get("/shipments", response_model=list[Shipment])
async def get_shipments():
    shipments = await shipments_collection.find().to_list(100)

    return [Shipment(**shipment) for shipment in shipments]








