import os
import json
from pathlib import Path

def remove_verts(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    for file in input_dir.glob("*.json"):
        with open(file, "r") as f:
            dictionary = json.load(f)

        dictionary.pop("verts", None)

        output_file = output_dir / file.name

        with open(output_file, "w") as f:
            json.dump(dictionary, f, indent=4)


# remove_verts("data", "cleansed_data")


path = r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\cleansed_data"
# path2 = r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\cleansed_data"
# remove_verts(path,path2)
# print("Json files edited")


def print10(input_dir):
    input_dir = Path(input_dir)
    # output_dir = Path(output_dir)

    # output_dir.mkdir(parents=True, exist_ok=True)
    count = 10
    for file in input_dir.glob("*.json"):
        if count != 0:
            with open(file, "r") as f:
                dictionary = json.load(f)
                print(dictionary)
            count-=1
            print("##################################")
        else:
            break

        # dictionary.pop("verts", None)

print10(path)