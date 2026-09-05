import json
from dataset_normalizer import HouseExpoNormalizer


DATASET_FILE = r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\cleansed_data\0a1a5807d65749c1194ce1840354be39.json"


def main():
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        house = json.load(f)

    normalizer = HouseExpoNormalizer()

    result = normalizer.normalize(house)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()