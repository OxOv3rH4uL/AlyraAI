from app.models.housePlan import HousePlan

class RenderingService:

    def render_svg(self,plan:HousePlan) -> str:
        """
        Converting House Plans to SVG Floor Plan
        """
        scale = 60
        padding = 25

        if not plan.rooms:
            return "<svg xmlns='http://www.w3.org/2000/svg'></svg>"

        #Finding the Max Height and Width and some calculation, it should be the resolution/dimensions of the image
        max_x = 0
        for room in plan.rooms:
            max_x = max(max_x,room.x+room.width)

        max_y = 0
        for room in plan.rooms:
            max_y = max(max_y,room.y+room.height)

        width = max_x * scale + padding * 2
        height = max_y * scale + padding * 2

        svg = [
            f"<svg xmlns='http://www.w3.org/2000/svg' "
            f"width='{width}' height='{height}' "
            f"viewBox='0 0 {width} {height}'>"
        ]

        svg.append(f"<rect width='100%' height='100%' fill='white'/>")

        for room in plan.rooms:
            x = room.x * scale + padding
            y = room.y * scale + padding
            room_width = room.width * scale
            room_height = room.height * scale 

            svg.append(
                f"<rect "
                f"x='{x}' "
                f"y='{y}' "
                f"width='{room_width}' "
                f"height='{room_height}' "
                f"fill='white' "
                f"stroke='black' "
                f"stroke-width='2'/>"
            )

            text_x = x + room_width / 2
            text_y = y + room_height / 2

            svg.append(
                f"<text "
                f"x='{text_x}' "
                f"y='{text_y}' "
                f"text-anchor='middle' "
                f"dominant-baseline='middle' "
                f"font-size='14'>"
                f"{room.name}"
                f"</text>"
            )

        svg.append("</svg>")

        return "".join(svg)
      
