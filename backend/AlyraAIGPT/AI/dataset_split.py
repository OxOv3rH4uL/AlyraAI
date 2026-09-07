import json
import random
from pathlib import Path

inputPath = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAI\backend\AlyraAIGPT\final_dataset\alpaca.json")
outputPath = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAI\backend\AlyraAIGPT\final_dataset")
TRAIN_RATIO = 0.90
VALIDATION_RATIO = 0.05
TEST_RATIO = 0.05

RANDOM_SEED = 42

def split():
    with open(inputPath,"r", encoding="utf-8") as f:
        dataset = json.load(f)

    random.seed(RANDOM_SEED)
    random.shuffle(dataset)
    total_samples = len(dataset)

    #Splitting the data for training, test and evaluation broski
    train_end = int(total_samples * TRAIN_RATIO)
    validation_end = train_end + int(total_samples * VALIDATION_RATIO)

    train_dataset = dataset[:train_end]
    validation_dataset = dataset[train_end:validation_end]
    test_dataset = dataset[validation_end:]
    files = {
        "train.json": train_dataset,
        "validation.json": validation_dataset,
        "test.json": test_dataset,
    }

    for filename, data in files.items():

        output_file = outputPath / filename

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )

    print("\nDataset split completed!")


if __name__ == "__main__":
    split()