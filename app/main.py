from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.auth import auth_router
from app.routes.users import users_router
from app.routes.sales import sales_router
from app.routes.productions import production_router
from app.routes.sop import sop_router
from app.routes.inventory import inventory_router
from app.routes.orders import orders_router
from app.routes.shipments import shipments_router
from app.database import connect_to_db, close_db_connection
from app.routes.websockets import websocket_router
from app.routes.decisioncontext import decision_context_router
import os



@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    yield
    await close_db_connection()

app = FastAPI(title="Logistics API", lifespan=lifespan)

# Routes
app.include_router(websocket_router, prefix="/ws", tags=["Websockets"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])
app.include_router(production_router, prefix="/production", tags=["Production"])
app.include_router(sop_router, prefix="/sop", tags=["S&OP"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(shipments_router, prefix="/shipments", tags=["Shipments"])
app.include_router(decision_context_router,prefix="/api")

    

@app.get("/")
async def root():
    return {"message": "Welcome to Logistics API"}

# Add at the end of the file
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", default=8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
