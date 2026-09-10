
import json
import sys


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

SCALE = 34

MARGIN_LEFT = 60
MARGIN_TOP = 90
MARGIN_RIGHT = 60
MARGIN_BOTTOM = 60

LEGEND_ROW_HEIGHT = 24


def build_svg(house_plan: dict, floor_index: int = 0) -> str:

    floor = house_plan["floor_plan"][floor_index]

    boundary = floor["boundary"]
    rooms = floor["rooms"]

    total_area = house_plan.get("total_area")

    bw = boundary["width"]
    bh = boundary["height"]

    canvas_w = bw * SCALE + MARGIN_LEFT + MARGIN_RIGHT
    canvas_h = (
        bh * SCALE
        + MARGIN_TOP
        + MARGIN_BOTTOM
        + LEGEND_ROW_HEIGHT
    )

    def X(x):
        return MARGIN_LEFT + x * SCALE

    def Y(y):
        return MARGIN_TOP + y * SCALE

    def W(w):
        return w * SCALE

    def H(h):
        return h * SCALE

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {canvas_w:.1f} {canvas_h:.1f}" '
        f'font-family="Helvetica, Arial, sans-serif">',

        f'<rect x="0" y="0" '
        f'width="{canvas_w:.1f}" '
        f'height="{canvas_h:.1f}" '
        f'fill="#FFFFFF"/>',

        f'<text x="{canvas_w / 2:.1f}" y="34" '
        f'font-size="22" '
        f'font-weight="700" '
        f'text-anchor="middle" '
        f'fill="#2C3E50">'
        f'One-Story House Plan'
        f'</text>',
    ]

    subtitle = f'Outer boundary: {bw:.2f} m × {bh:.2f} m'

    if total_area is not None:
        subtitle = (
            f'Total area: {total_area:.2f} m²  |  '
            + subtitle
        )

    parts.append(
        f'<text x="{canvas_w / 2:.1f}" y="56" '
        f'font-size="13" '
        f'text-anchor="middle" '
        f'fill="#7B7D7D">'
        f'{subtitle}'
        f'</text>'
    )

    # Exterior wall
    parts.append(
        f'<rect '
        f'x="{X(0):.1f}" '
        f'y="{Y(0):.1f}" '
        f'width="{W(bw):.1f}" '
        f'height="{H(bh):.1f}" '
        f'fill="none" '
        f'stroke="#1B2631" '
        f'stroke-width="4"/>'
    )

    # Rooms
    used_types = []

    for room in rooms:

        rtype = room.get(
            "room_type",
            room.get("name", "Room")
        )

        color = ROOM_COLORS.get(
            rtype,
            DEFAULT_COLOR
        )

        if rtype not in used_types:
            used_types.append(rtype)

        px = X(room["x"])
        py = Y(room["y"])

        pw = W(room["width"])
        ph = H(room["height"])

        # Room rectangle
        parts.append(
            f'<rect '
            f'x="{px:.1f}" '
            f'y="{py:.1f}" '
            f'width="{pw:.1f}" '
            f'height="{ph:.1f}" '
            f'fill="{color}" '
            f'stroke="#1B2631" '
            f'stroke-width="2"/>'
        )

        # --------------------------------
        # Room label
        # --------------------------------

        label = room.get("name", rtype)
        label = label.replace("_", " ")

        cx = px + pw / 2
        cy = py + ph / 2

        # Choose font size based on room size
        room_size = min(pw, ph)

        if room_size < 70:
            font_size = 9
        elif room_size < 110:
            font_size = 11
        else:
            font_size = 13

        # Maximum characters that can fit
        max_chars = max(
            6,
            int(pw / (font_size * 0.6))
        )

        # Wrap long labels
        words = label.split()

        lines = []
        current_line = ""

        for word in words:

            test_line = (
                word
                if not current_line
                else current_line + " " + word
            )

            if len(test_line) <= max_chars:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

        # Vertical centering
        line_height = font_size + 3

        start_y = (
            cy
            - ((len(lines) - 1) * line_height) / 2
            + font_size / 3
        )

        for index, line in enumerate(lines):

            text_y = start_y + index * line_height

            parts.append(
                f'<text '
                f'x="{cx:.1f}" '
                f'y="{text_y:.1f}" '
                f'font-size="{font_size}" '
                f'font-weight="600" '
                f'text-anchor="middle" '
                f'fill="#1B2631">'
                f'{line}'
                f'</text>'
            )

    # --------------------------------
    # Legend
    # --------------------------------

    legend_y = (
        canvas_h
        - MARGIN_BOTTOM
        + 20
    )

    lx = MARGIN_LEFT

    for rtype in used_types:

        color = ROOM_COLORS.get(
            rtype,
            DEFAULT_COLOR
        )

        label = rtype.replace("_", " ")

        parts.append(
            f'<rect '
            f'x="{lx:.1f}" '
            f'y="{legend_y:.1f}" '
            f'width="14" '
            f'height="14" '
            f'fill="{color}" '
            f'stroke="#1B2631" '
            f'stroke-width="1"/>'
        )

        parts.append(
            f'<text '
            f'x="{lx + 18:.1f}" '
            f'y="{legend_y + 11:.1f}" '
            f'font-size="11" '
            f'fill="#2C3E50">'
            f'{label}'
            f'</text>'
        )

        lx += (
            18
            + len(label) * 6.5
            + 20
        )

    parts.append("</svg>")

    return "\n".join(parts)

SAMPLE = {"total_area":102.345,"status":"normalized","floors":1,"floor_plan":[{"floor":1,"boundary":{"width":10.86,"height":9.45},"rooms":[{"name":"Bedroom","room_type":"Bedroom","x":0,"y":0,"width":5.22,"height":5.22},{"name":"Living_Room","room_type":"Living_Room","x":5.1,"y":0,"width":5.76,"height":5.22},{"name":"Kitchen","room_type":"Kitchen","x":0,"y":5.13,"width":5.22,"height":4.32},{"name":"Child_Room","room_type":"Child_Room","x":5.1,"y":5.13,"width":5.76,"height":4.32},{"name":"Toilet","room_type":"Toilet","x":5.1,"y":5.13,"width":2.69,"height":2.69}]}]}


def main():

    if len(sys.argv) >= 2:

        with open(sys.argv[1], "r") as f:
            house_plan = json.load(f)

    else:
        house_plan = SAMPLE
        # print("No house plan JSON provided.")
        # return

    out_path = (
        sys.argv[2]
        if len(sys.argv) >= 3
        else "house_plan2.svg"
    )

    svg = build_svg(house_plan)
    print(svg)
    with open(out_path, "w") as f:
        f.write(svg)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
