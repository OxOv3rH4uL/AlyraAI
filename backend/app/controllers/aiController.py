from app.schemas.planSchema import PlanRequest,PlanResponse
from app.services.aiService import AIService

class AIController:
    def __init__(self,aiService:AIService):
        self.aiService = aiService

    def generate_plan(self,req:PlanRequest) -> PlanResponse:
        return self.aiService.generate_plan(req)