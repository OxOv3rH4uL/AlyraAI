from fastapi import FastAPI
from app.schemas.planSchema import PlanRequest, PlanResponse
from backend.app.services.planServiceMock import PlanService
from app.controllers.planController import PlanController
from app.services.layoutValidator import LayoutValidator
from app.services.layoutService import LayoutService
from app.services.renderingService import RenderingService

app = FastAPI(
    title="Alyra House Planner Backend API",
    description="Converting Housing Ideas to Housing Plans",
    version="0.1"
)
layoutValidator = LayoutValidator()
layoutService = LayoutService()
renderer = RenderingService()
planService = PlanService(layoutService=layoutService,validator=layoutValidator,renderer=renderer)
planController = PlanController(planService=planService)

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


@app.get("/api/v1/plans/generate", response_model=PlanResponse)
def generate_plan(req: PlanRequest):
    return planController.generate_plan(req)

