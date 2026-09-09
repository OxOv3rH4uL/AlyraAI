# from app.models.housePlan import HousePlan
# from app.schemas.planSchema import PlanResponse
from app.schemas.testSchema import HousePlan,Room
# from app. import HousePlan

import json
import sys

class RenderingService:

    def render_svg(self, house_plan: HousePlan,floor_index:int = 0) -> str:
        """
        Convert a HousePlan into an SVG floor plan.
        """
        # Color palette per room_type. Unrecognized types fall back to a neutral gray.
        ROOM_COLORS = {
            "Bedroom": "#AED6F1",
            "Room": "#D5DBDB",
            "Toilet": "#F9E79F",
            "Bathroom": "#F9E79F",
            "Kitchen": "#F5B7B1",
            "Living_Room": "#A9DFBF",
            "Dining_Room": "#F8C471",
            "Hallway": "#D2B4DE",
            "Balcony": "#A3E4D7",
            "Garage": "#CCD1D1",
            "Study": "#FADBD8",
        }
        DEFAULT_COLOR = "#EAECEE"

        SCALE = 34          # pixels per plan unit (meter)
        MARGIN_LEFT = 60
        MARGIN_TOP = 90
        MARGIN_RIGHT = 60
        MARGIN_BOTTOM = 60
        LEGEND_ROW_HEIGHT = 24
        house_plan = HousePlan.model_validate(house_plan)
        floor = house_plan.floor_plan[floor_index]
        boundary = floor.boundary
        rooms = floor.rooms
        total_area = house_plan.total_area
    
        bw, bh = boundary.width, boundary.height
        canvas_w = bw * SCALE + MARGIN_LEFT + MARGIN_RIGHT
        canvas_h = bh * SCALE + MARGIN_TOP + MARGIN_BOTTOM + LEGEND_ROW_HEIGHT
    
        def X(x): return MARGIN_LEFT + x * SCALE
        def Y(y): return MARGIN_TOP + y * SCALE
        def W(w): return w * SCALE
        def H(h): return h * SCALE
    
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w:.1f} {canvas_h:.1f}" '
            f'font-family="Helvetica, Arial, sans-serif">',
            f'<rect x="0" y="0" width="{canvas_w:.1f}" height="{canvas_h:.1f}" fill="#FFFFFF"/>',
            f'<text x="{canvas_w/2:.1f}" y="34" font-size="22" font-weight="700" '
            f'text-anchor="middle" fill="#2C3E50">Generated House Plan</text>',
        ]
    
        subtitle = f'Outer boundary: {bw:.2f} m &#215; {bh:.2f} m'
        if total_area is not None:
            subtitle = f'Total area: {total_area:.2f} m&#178;  |  ' + subtitle
        parts.append(
            f'<text x="{canvas_w/2:.1f}" y="56" font-size="13" text-anchor="middle" '
            f'fill="#7B7D7D">{subtitle}</text>'
        )
    
        # Exterior wall
        parts.append(
            f'<rect x="{X(0):.1f}" y="{Y(0):.1f}" width="{W(bw):.1f}" height="{H(bh):.1f}" '
            f'fill="none" stroke="#1B2631" stroke-width="4"/>'
        )
    
        # Rooms
        used_types = []
        for room in rooms:
            # rtype = room.get("room_type", room.get("name", "Room"))
            rtype = room.room_type
            color = ROOM_COLORS.get(rtype, DEFAULT_COLOR)
            if rtype not in used_types:
                used_types.append(rtype)
    
            px, py = X(room.x), Y(room.y)
            pw, ph = W(room.width), H(room.height)
            parts.append(
                f'<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" '
                f'fill="{color}" stroke="#1B2631" stroke-width="2"/>'
            )
    
            label = room.name.replace("_", " ")
            area = room.width * room.height
            cx, cy = px + pw / 2, py + ph / 2
            parts.append(
                f'<text x="{cx:.1f}" y="{cy-6:.1f}" font-size="13" font-weight="600" '
                f'text-anchor="middle" fill="#1B2631">{label}</text>'
            )
            parts.append(
                f'<text x="{cx:.1f}" y="{cy+12:.1f}" font-size="11" text-anchor="middle" '
                f'fill="#34495E">{room.width:.2f} &#215; {room.height:.2f} m ({area:.1f} m&#178;)</text>'
            )
    
        # Legend
        legend_y = canvas_h - MARGIN_BOTTOM + 20
        lx = MARGIN_LEFT
        for rtype in used_types:
            color = ROOM_COLORS.get(rtype, DEFAULT_COLOR)
            label = rtype.replace("_", " ")
            parts.append(
                f'<rect x="{lx:.1f}" y="{legend_y:.1f}" width="14" height="14" '
                f'fill="{color}" stroke="#1B2631" stroke-width="1"/>'
            )
            parts.append(
                f'<text x="{lx+18:.1f}" y="{legend_y+11:.1f}" font-size="11" fill="#2C3E50">{label}</text>'
            )
            lx += 18 + len(label) * 6.5 + 20
    
        parts.append('</svg>')
        return "\n".join(parts)
        
              


# renderer = RenderingService()

# res = {"total_area":102.348,"status":"normalized","floors":1,"floor_plan":[{"floor":1,"boundary":{"width":10.2,"height":10.04},"rooms":[{"name":"Bathroom","room_type":"Bathroom","x":0,"y":5.1,"width":5.19,"height":4.94},{"name":"Kitchen","room_type":"Kitchen","x":5.07,"y":0,"width":5.13,"height":5.22},{"name":"Bedroom","room_type":"Bedroom","x":0,"y":0,"width":5.19,"height":5.22}]}]}
# plan= HousePlan.model_validate(res)
# print(plan)

# res = {"total_area":107.248,"status":"normalized","floors":1,"floor_plan":[{"floor":1,"boundary":{"width":10.36,"height":10.3},"rooms":[{"name":"Toilet","room_type":"Toilet","x":5.13,"y":0,"width":5.23,"height":5.22},{"name":"Kitchen","room_type":"Kitchen","x":0,"y":0,"width":5.22,"height":5.22},{"name":"Bedroom","room_type":"Bedroom","x":0,"y":5.13,"width":5.22,"height":5.17},{"name":"Living_Room","room_type":"Living_Room","x":5.13,"y":5.13,"width":5.23,"height":5.17}]}]}


# print(renderer.render_svg(plan))