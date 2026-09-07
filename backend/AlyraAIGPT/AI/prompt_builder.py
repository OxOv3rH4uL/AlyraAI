# def build_prompt(requirements):
#     floors = requirements["floors"]
#     rooms = requirements["rooms"]

#     room_list = "\n".join(rooms)

#     prompt = f"""
# You are generating training data for a house-planning AI.

# Given the number of floors and the list of rooms, generate ONE simple,
# natural-language request that a real person might give to an AI house planner.


# IMPORTANT:
# Each request should sound different from previous requests.

# Choose ONE of these styles randomly:
# 1. Direct request
# 2. Casual request
# 3. Detailed requirement
# 4. Short/simple request
# 5. "I am looking for..." style
# 6. "I need..." style
# 7. "Can you create..." style
# 8. "Help me design..." style
# 9. Family/home requirement style
# 10. Conversational style


# Rules:
# 1. Mention EVERY room provided.
# 2. Do NOT omit any room.
# 3. Do NOT add any room that is not provided.
# 4. Do NOT mention dimensions, measurements, areas, or coordinates.
# 5. Do NOT describe the position or relationship between rooms.
# 6. Do NOT invent any requirements or features.
# 7. Keep the room names simple and natural.
# 8. Keep the sentence short and easy to understand.
# 9. Mention the correct number of floors.
# 10. Do NOT include explanations, markdown, or extra text.
# 11. Write like a real person asking an AI to design this house.
# 12. Do not mention that you are generating the data
# 13. Return ONLY valid JSON.
# 14. Do not always start with "Could you please design".
# 15. Do not always use "one-story house".


# Input:
# Floors: {floors}

# Rooms:
# {room_list}

# Output format:
# {{
#   "request": "..."
# }}
# """

#     return prompt


import random
import json

OPENERS = [
    "I need a house with {rooms}.",
    "Can you design a home that has {rooms}?",
    "Looking for a house with {rooms}.",
    "Help me plan a house with {rooms}.",
    "I want to build a house that includes {rooms}.",
    "Design a house containing {rooms}.",
    "We're planning a home with {rooms}.",
    "Please create a house layout with {rooms}.",
    "I'd like a house that has {rooms}.",
    "Make me a house plan with {rooms}.",
]

FLOOR_PHRASES = {
    1: ["single-story", "one-level", "single-floor", "ground-floor only", "all on one level"],
    2: ["two-story", "two-level", "double-floor", "with an upstairs"],
    3: ["three-story", "three-level", "multi-level"],
}

def build_prompt(requirements):
    floors = requirements["floors"]
    rooms = requirements["rooms"]
    room_list = "\n".join(rooms)
    
    opener = random.choice(OPENERS)
    room_list = ", ".join(rooms)
    filled = opener.format(rooms=room_list)

    return f"""Rewrite the sentence below so it reads naturally, like something a real person would type to an AI house planner. Keep it about the same length. Do not add rooms, dimensions, positions, floors, coordinates, or areas.

Example
Input: Can you design a home that has living room, garage.
Output: Help me design a home with a living room and a garage.

Now do the same.
Input: {filled}
Output:"""