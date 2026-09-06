def extract_floors_rooms(house_plan):
  floors = house_plan["floors"]

  room_types = []

  for floor in house_plan["floor_plan"]:
      for room in floor["rooms"]:
          room_type = room["room_type"]

          if room_type not in room_types:
              room_types.append(room_type)

  return {
      "floors": floors,
      "rooms": room_types
  }

