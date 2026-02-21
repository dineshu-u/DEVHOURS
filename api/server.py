from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from flow_guardian_x.api import routes_predict, routes_route, routes_emergency, routes_intelligence, routes_chaos
from flow_guardian_x.config import API_HOST, API_PORT

app = FastAPI(title="Flow Guardian X API", description="Predictive Traffic Intelligence & Optimization")

# CORS — allow dashboard (file://) and any localhost origin to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include Routers
app.include_router(routes_predict.router, prefix="/api/v1")
app.include_router(routes_route.router, prefix="/api/v1")
app.include_router(routes_emergency.router, prefix="/api/v1")
app.include_router(routes_intelligence.router, prefix="/api/v1")
app.include_router(routes_chaos.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Flow Guardian X API. Traffic intelligence at its best."}

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
