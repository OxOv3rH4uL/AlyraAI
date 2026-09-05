from pathlib import Path

from pathlib import Path
import json

from dataset_analyzer import DatasetAnalyzer
from dataset_statistics import DatasetStatistics
from relationship_statistics import DatasetRelationshipStatistics
from dataset_normalizer import HouseExpoNormalizer


DATASET_PATH = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\cleansed_data")
# DATASET_PATH = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\example_data")
# OUTPUT_FILE = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\analysis_results.txt")
op2 = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\statistics_results.txt")
# op2 = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\relationship_results.txt")
# op2 = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\example_results.txt")


def main():

    analyzer = DatasetAnalyzer()
    stat = DatasetStatistics()
    normalizer = HouseExpoNormalizer()
    # stat = DatasetRelationshipStatistics()  
    json_files = list(DATASET_PATH.glob("*.json"))
    for file in json_files:

        with open(file, "r", encoding="utf-8") as f:
            house = json.load(f)
        analyzed = analyzer.analyze(house)
        # normalized = normalizer.normalize(house)

        stat.add_house(analyzed)

    summary = stat.summary()

    with open(op2, "w", encoding="utf-8") as output:
        output.write(
            json.dumps(summary, indent=2)
        )

    print(f"Analyzed {len(json_files)} houses")
    print(f"Results saved to: {op2}")

if __name__ == "__main__":
    main()