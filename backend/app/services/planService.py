from sqlalchemy.orm import Session
from app.schemas.planSchema import PlanRequest
from app.schemas.aiSchema import AIPlanResponse
from app.services.aiService import AIService
from app.services.layoutService import LayoutService
from app.services.layoutValidator import LayoutValidator
from app.services.renderingService import RenderingService
from app.repositories.planRepository import PlanRepository


class PlanService:
    def __init__(self,db:Session):
        self.ai_service = AIService()
        self.validator = LayoutValidator()
        self.renderer = RenderingService()
        self.repo = PlanRepository()

    def generate_plan(self, plan: PlanRequest) -> AIPlanResponse:

        #step 1: ai generating the plan
        plan = self.ai_service.generate_plan(plan)
        #step 2: validate the layout if not send back to AI to do it again
        errors = self.validator.validate(plan)
        if errors:
            raise ValueError(
                f"Invalid House Plan :{errors}"
            )
        
        #step 3: Render SVG
        for floor_plan in plan.floor_plans:

            floor_plan.svg = (
                self.renderer.render_floor_svg(
                    floor_plan
                )
            )
        #step 4: Save to DB
        last_plan = self.repo.save(plan)
        return last_plan
        