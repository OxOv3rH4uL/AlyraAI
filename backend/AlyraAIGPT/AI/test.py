import json
import subprocess


job = {
    "house_id": "test-001",
    "house_plan": {
        "total_area": 77.1528,
        "status": "normalized",
        "floors": 1,
        "floor_plan": [
            {
                "floor": 1,
                "boundary": {
                    "width": 10.54,
                    "height": 7.32
                },
                "rooms": [
                    {
                        "name": "Storage",
                        "room_type": "Storage",
                        "x": 0.0,
                        "y": 6.06,
                        "width": 2.88,
                        "height": 1.21
                    },
                    {
                        "name": "Toilet",
                        "room_type": "Toilet",
                        "x": 0.0,
                        "y": 2.8,
                        "width": 2.88,
                        "height": 2.32
                    }
                ]
            }
        ]
    }
}


process = subprocess.Popen(
    ["python", "qwen.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

output, _ = process.communicate(
    json.dumps(job) + "\n"
)

print("Result:")
print(output)