from app.schemas.planSchema import PlanRequest
from app.schemas.aiSchema import AIPlanResponse

class AIService:
    def generate_plan(self,req:PlanRequest) -> AIPlanResponse:
        """
        Main model generating the plan according to the user request
        """
        pass
