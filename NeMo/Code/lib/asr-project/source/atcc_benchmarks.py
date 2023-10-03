import os
import json
import torch
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
from models import PretrainedFineTunedJasper
from data import Data, ATCCompleteData, split_data

torch.set_float32_matmul_precision("high")
plt.style.use("ggplot")


def split_train_set(training_set: Data, split_ratio=0.2) -> List[Data]:
    train_data_splits = []
    # calculate how many iterations it will take to cover the entire dataset
    iterations = int(1.0 / split_ratio)

    current_split = split_ratio
    for i in range(iterations):
        # calculate length of this split
        data_length = int(len(training_set.data) * current_split)

        # add current split to return list
        train_data_splits.append(Data.from_iterable(training_set.data[:data_length]))

        # increment to next split
        current_split += split_ratio

    return train_data_splits


if __name__ == "__main__":
    results = {"results": []}
    # Path to root of ATCC
    atcc_path = "/home/students/vandebra/programming/thesis_data/atc0_comp"
    # initialize atcc dataset utility
    atcc = ATCCompleteData(data_root=atcc_path, random_seed=1)

    # parse the transcripts into a common format
    atcc.parse_transcripts()

    train, test = split_data(atcc, test=True, validation=False, test_split_ratio=0.2)
    train_splits = split_train_set(train, split_ratio=0.2)

    test.dump_manifest("atcc_benchmarks/atcc_test.json")

    for i, split in enumerate(train_splits):
        checkpoint_path = f"atcc_benchmarks/jasper_train_split={i}.nemo"
        train_manifest = f"atcc_benchmarks/atcc_train_split={i}.json"

        # create model
        model = PretrainedFineTunedJasper(checkpoint_path=checkpoint_path)

        # set up training data
        model.training_setup(
            training_manifest_path=train_manifest, accelerator="gpu", max_epochs=150,
        )

        if not os.path.exists(checkpoint_path):
            # dump training split to manifest
            split.dump_manifest(train_manifest)
            # start training loop
            model.fit()

        model.testing_setup(test_manifest_path="atcc_benchmarks/atcc_test.json")

        test_wer = model.test(testing_set="test")
        train_wer = model.test(testing_set="train")

        results["results"].append(
            {
                "checkpoint": checkpoint_path,
                "test_wer": test_wer,
                "train_wer": train_wer,
                "epochs": 150,
                "training_manifest": train_manifest,
                "test_manifest": "atcc_benchmarks/atcc_test.json",
                "test_split_ratio": 0.2,
                "train_split_ratio": 0.2 * (i + 1),
                "train_samples": split.num_samples,
                "test_samples": test.num_samples,
            }
        )

    datapoints = pd.DataFrame(
        columns=[
            "Model/Data Split Number",
            "WER on Test Set",
            "WER on Train Set",
            "# of Training Samples",
            "% of Total Training Data",
        ]
    )

    fig, ax = plt.subplots()
    ax.set_title("WER vs Number of Training Samples")
    ax.set_xlabel("# Training Samples")
    ax.set_ylabel("WER on Test Set")

    for i, train_results in enumerate(results["results"]):
        datapoints.loc[i + 1] = [
            train_results["checkpoint"],
            train_results["test_wer"],
            train_results["train_wer"],
            train_results["train_samples"],
            train_results["train_split_ratio"] * 100,
        ]

        # y-axis: WER, x-axis: samples
        ax.scatter(
            train_results["train_samples"],
            train_results["test_wer"],
            label=f"{int(train_results['train_split_ratio'] * 100)} % of training data",
        )

    # y-axis: WER, x-axis: samples
    ax.plot(
        [train_results["train_samples"] for train_results in results["results"]],
        [train_results["test_wer"] for train_results in results["results"]],
    )

    ax.legend()

    with open("atcc_benchmarks/results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    datapoints.to_excel("atcc_benchmark_results.xlsx")
    plt.savefig("atcc_benchmarks.svg", format="svg")
    plt.show()
