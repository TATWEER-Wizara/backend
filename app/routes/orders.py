"""
Orders Routes Module

This module handles all order-related API endpoints including CRUD operations
for order management.

Endpoints:
    - POST /orders: Create new order
    - GET /orders/{order_id}: Retrieve specific order
    - PUT /orders/{order_id}: Update order
    - DELETE /orders/{order_id}: Remove order
    - GET /orders: List all orders
"""

# crud for orders

from fastapi import APIRouter, HTTPException
from app.models.orders import Order
from app.database import orders_collection
from bson import ObjectId
from datetime import datetime

orders_router = APIRouter()

@orders_router.post("/orders", response_model=Order)
async def create_order(order: Order):
    """
    Create a new order.

    Args:
        order (Order): Order data to create

    Returns:
        Order: Created order record with ID

    Raises:
        HTTPException: If creation fails
    """
    order_dict = order.model_dump()
    order_dict["created_at"] = datetime.now(datetime.UTC)

    new_order = await orders_collection.insert_one(order_dict)
    return Order(**order_dict, id=str(new_order.inserted_id))


@orders_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await orders_collection.find_one({"_id": ObjectId(order_id)})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order)


@orders_router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, order: Order):
    order_dict = order.model_dump()

    order_dict["updated_at"] = datetime.now(datetime.UTC)
    await orders_collection.update_one({"_id": ObjectId(order_id)}, {"$set": order_dict})
    return Order(**order_dict, id=str(order_id))

@orders_router.delete("/orders/{order_id}", response_model=Order)
async def delete_order(order_id: str):
    order = await orders_collection.find_one({"_id": ObjectId(order_id)})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await orders_collection.delete_one({"_id": ObjectId(order_id)})
    return Order(**order)


@orders_router.get("/orders", response_model=list[Order])
async def get_orders():
    orders = await orders_collection.find().to_list(100)
    return [Order(**order) for order in orders]




