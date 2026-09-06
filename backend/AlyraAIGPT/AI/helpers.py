import re
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


def clean_output(text: str) -> str:
    BANNED_PATTERNS = [
        r'^(sure|okay|ok|certainly)[,!:.]?\s*',
        r'^(no preamble.*?)\n+', 
        r'^(request|output|answer)\s*[:\-]\s*',
        r"^(sure|okay|ok|certainly|of course|here you go|here's|here is)[,!:.]?\s*",
        r"^here'?s a (natural[- ]sounding )?(version|request|rewrite)[^:]*:\s*",
        r"^(natural[- ]sounding version|rewritten sentence)[:\s]*",
        r'^(i\'?d rewrite (it|this) as|this could be phrased as|you could say|how about)[:\s]*',
        r'^(let me rewrite|let\'s rewrite|rewriting (it|this))[^:]*:?\s*',
        r'^as an ai[^,]*,\s*',
        r'^(sentence|input|output)\s*:\s*',
    ]
    text = text.strip()

    prev = None
    while prev != text:
        prev = text
        for pat in BANNED_PATTERNS:
            text = re.sub(pat, '', text, flags=re.IGNORECASE).strip()

    m = re.search(r'"request"\s*:\s*"([^"]+)"', text)
    if m:
        text = m.group(1)

    text = text.strip('"\'` ')

    text = text.split("\n")[0].strip()
    return text


def is_still_bad(text: str) -> bool:
    """Lightweight safety net after clean_output — plain substring check, not regex."""
    bad_starts = (
        "sure", "okay", "ok,", "certainly", "here", "as an ai",
        "natural-sounding", "rewritten", "request:", "output:",
    )
    low = text.lower()
    return len(text) < 10 or any(low.startswith(b) for b in bad_starts)