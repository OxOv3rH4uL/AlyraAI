<!-- You are generating training data for a house-planning AI.

Given the following HousePlan JSON, generate a realistic natural-language
user request that describes the requirements represented by this house plan.

Rules:
1. Mention only rooms that exist in the HousePlan.
2. Do not invent rooms.
3. Do not invent dimensions, relationships, or requirements.
4. Keep the request natural, like a real person asking an AI to design a house.
5. Do not mention coordinates.
6. Do not mention that the request was generated from an existing plan.
7. Return only the requested JSON format.

HousePlan:
{HOUSE_PLAN_JSON} -->

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
Floors: <number>

Rooms:
<room 1>
<room 2>
<room 3>
...

Output format:
{
  "request": "..."
}