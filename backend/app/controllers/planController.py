from app.schemas.planSchema import PlanRequest, PlanResponse
from backend.app.services.planServiceMock import PlanService

class PlanController:
    def __init__(self,planService: PlanService):
        self.planService = planService

    def generate_plan(self,req: PlanRequest) -> PlanResponse:
        return self.planService.generate_plan(req)