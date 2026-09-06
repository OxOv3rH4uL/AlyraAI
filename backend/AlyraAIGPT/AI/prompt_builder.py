def build_prompt(requirements):
    floors = requirements["floors"]
    rooms = requirements["rooms"]

    room_list = "\n".join(rooms)

    prompt = f"""
You are generating training data for a house-planning AI.

Given the number of floors and the list of rooms, generate ONE simple,
natural-language request that a real person might give to an AI house planner.

Rules:
1. Mention EVERY room provided.
2. Do NOT omit any room.
3. Do NOT add any room that is not provided.
4. Do NOT mention dimensions, measurements, areas, or coordinates.
5. Do NOT describe the position or relationship between rooms.
6. Do NOT invent any requirements or features.
7. Keep the room names simple and natural.
8. Keep the sentence short and easy to understand.
9. Mention the correct number of floors.
10. Return ONLY valid JSON.
11. Do NOT include explanations, markdown, or extra text.

Input:
Floors: {floors}

Rooms:
{room_list}

Output format:
{{
  "request": "..."
}}
"""

    return prompt