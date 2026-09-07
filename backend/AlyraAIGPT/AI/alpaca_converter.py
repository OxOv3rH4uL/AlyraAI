import pathlib
import json

def is_valid_request(request):

    if not isinstance(request, str):
        return False

    request = request.strip()

    if not request:
        return False

    if len(request) < 15:
        return False

    bad_patterns = [
        "the rewritten version:",
        "rewritten version:",
        "here is the rewritten",
        "here's the rewritten",
        "rewritten request",
        "revised request",
        "revised version",
        "the revised version",
        "here is the revised",
        "here's the revised",
        "here is the request",
        "here's the request",
        "the request is",
        "user request:",
        "user's request:",
        "user request",
        "the user's request",
        "the user wants",
        "the user needs",
        "how",
        "based on the request",
        "based on the user's request",
        "based on the house plan",
        "based on the provided",
        "as requested",
        "as per the request",
    ]

    request_lower = request.lower()

    for pattern in bad_patterns:
        if pattern in request_lower:
            return False

    return True

def alpaca_converter():
    inputPath = pathlib.Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAI\backend\AlyraAIGPT\ai_dataset")
    outputPath = pathlib.Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAI\backend\AlyraAIGPT\final_dataset\alpaca.json")

    INSTRUCTION = (
    "Generate a HousePlan JSON based on the user's house requirements."
    )

    samples = []
    json_files = list(inputPath.glob("*.json"))

    for i, fp in enumerate(json_files,start=1):
        try:
            with open(fp, "r", encoding="utf-8") as file:
                data = json.load(file)

                request = data["request"]
                if not is_valid_request(request):
                    continue
                house_plan = data["house_plan"]

                sample = {
                    "instruction": INSTRUCTION,
                    "input": request,
                    "output": json.dumps(
                        house_plan,
                        separators=(",", ":")
                    )
                }

                samples.append(sample)

        except Exception as e:
            print(f"Skipping {fp.name}: {e}")

        if i % 1000 == 0:
            print(f"Processed {i} files...")

    outputPath.parent.mkdir(parents=True, exist_ok=True)
    with open(outputPath, "w", encoding="utf-8") as file:
        json.dump(
            samples,
            file,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("Conversion completed!")
    print(f"Total samples: {len(samples)}")
    


if __name__ == "__main__":
    alpaca_converter()
