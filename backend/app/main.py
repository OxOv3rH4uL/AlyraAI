from fastapi import FastAPI
from app.schemas.planSchema import PlanRequest, PlanResponse
from app.services.renderingService import RenderingService
from app.services.aiService import AIService
from app.controllers.aiController import AIController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Alyra House Planner Backend API",
    description="Converting Housing Ideas to Housing Plans",
    version="0.1"
)


origins =[
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


renderer = RenderingService()
planService = AIService(renderer)
planController = AIController(planService)


@app.get("/")
def root():
    return {
        "message": "Backend API is running bro"
    }

@app.get("/heartBeat")
def health():
    return {
        "message":"Alive!"
    }


@app.post("/api/v1/plans/generate")
def generate_plan(req: PlanRequest):
    
    # return req;
    return planController.generate_plan(req)

