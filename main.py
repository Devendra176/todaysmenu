import uvicorn
from fastapi import FastAPI
from user.routes import router as user_router
from customer.routes import router as customer_router
from restaurant.routes import router as owner_router
from restaurant.menu.routes import router as menu_router

app = FastAPI(
    title="Today's Menu APIs",
    description="This is a custom description of my API",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Operations related to users"},
        {"name": "customers", "description": "Operations related to customers"},
        {"name": "restaurants", "description": "Operations related to restaurants"},
    ]
)

app.include_router(user_router, prefix="/auth", tags=["auth"])
app.include_router(customer_router, prefix="/customer", tags=["customers"])
app.include_router(owner_router, prefix="/restaurant", tags=["restaurants"])
app.include_router(menu_router, prefix="/restaurant", tags=["restaurants"])

if __name__ == "__main__":
    uvicorn.run(app)
