from fastapi import APIRouter
from app.database import sales_collection, production_collection, sop_collection
from app.models.sop import SOP
import datetime
from datetime import UTC

sop_router = APIRouter()


@sop_router.post("/sop")
async def generate_sop_plan():

    # Récupération des ventes et productions
    sales = await sales_collection.find().to_list(100)
    production = await production_collection.find().to_list(100)

    forecasted_demand = {}
    production_capacity = {}

    # Agrégation des données
    for sale in sales:
        product = sale["product_id"]
        forecasted_demand[product] = forecasted_demand.get(product, 0) + sale["quantity"]

    for prod in production:
        product = prod["product_id"]
        production_capacity[product] = production_capacity.get(product, 0) + prod["quantity_produced"]

    # Création du plan
    sop_plan = SOP(
        forecasted_demand=forecasted_demand,
        production_capacity=production_capacity
    )


    await sop_collection.insert_one(sop_plan.model_dump())

    return {"message": "S&OP Plan created", "sop_plan": sop_plan.model_dump()}
