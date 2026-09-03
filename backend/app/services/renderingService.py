from app.models.housePlan import FloorPlan


class RenderingService:
    #AI is used for this god who knows how svg internally works already this project is too complex
    SCALE = 20
    PADDING = 40

    def render_floor_svg(self, floor_plan: FloorPlan) -> str:

        boundary = floor_plan.boundary

        svg_width = (
            boundary.width * self.SCALE
            + self.PADDING * 2
        )

        svg_height = (
            boundary.height * self.SCALE
            + self.PADDING * 2
        )

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{svg_width}" '
            f'height="{svg_height}" '
            f'viewBox="0 0 {svg_width} {svg_height}">'
        ]

        
        svg.append(
            f'<rect '
            f'x="{self.PADDING}" '
            f'y="{self.PADDING}" '
            f'width="{boundary.width * self.SCALE}" '
            f'height="{boundary.height * self.SCALE}" '
            f'fill="none" '
            f'stroke="black"/>'
        )

        
        for room in floor_plan.rooms:

            x = room.x * self.SCALE + self.PADDING
            y = room.y * self.SCALE + self.PADDING

            width = room.width * self.SCALE
            height = room.height * self.SCALE

            svg.append(
                f'<rect '
                f'x="{x}" '
                f'y="{y}" '
                f'width="{width}" '
                f'height="{height}" '
                f'fill="none" '
                f'stroke="black"/>'
            )

            text_x = x + width / 2
            text_y = y + height / 2

            svg.append(
                f'<text '
                f'x="{text_x}" '
                f'y="{text_y}" '
                f'text-anchor="middle" '
                f'dominant-baseline="middle">'
                f'{room.name}'
                f'</text>'
            )

        svg.append('</svg>')

        return ''.join(svg)