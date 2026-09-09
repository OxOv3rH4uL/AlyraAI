from app.schemas.planSchema import PlanRequest,PlanResponse
import requests,json
from app.services.renderingService import RenderingService
# from app.models.housePlan import HousePlan
from app.schemas.testSchema import HousePlan
class AIService:

    def __init__(self,renderer:RenderingService):
        self.renderer = renderer
    def generate_plan(self,req:PlanRequest) -> PlanResponse:
        """
        Main model generating the plan according to the user request
        """
        desc = req.description
        res = requests.post("http://localhost:8001/generate",
                            json={
                                "request":desc
                            })
        data = res.json()
        hp = data["house_plan"]
        if isinstance(hp, str):
            hp = json.loads(hp)
        house_plan = HousePlan.model_validate(hp)
        svg = self.renderer.render_svg(house_plan)
        hp["svg"] = svg
        return hp

        
