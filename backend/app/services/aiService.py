from app.schemas.planSchema import PlanRequest
from app.schemas.aiSchema import AIPlanResponse
from app.models.housePlan import HousePlan

class AIService:
    def generate_plan(self,req:PlanRequest) -> HousePlan:
        """
        Main model generating the plan according to the user request
        """
        pass
