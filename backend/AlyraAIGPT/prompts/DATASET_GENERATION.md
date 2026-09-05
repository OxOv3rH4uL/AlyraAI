You are generating training data for a house-planning AI.

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
{HOUSE_PLAN_JSON}