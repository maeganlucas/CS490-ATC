import json

from data import *
from models import *

RANDOM_SEED = 1

models = [
    ("checkpoints/ctc_randominit.nemo", RandomInitCTC),
    ("checkpoints/jasper_finetuned.nemo", PretrainedFineTunedJasper),
    ("checkpoints/jasper_pretrained.nemo", PretrainedJasper),
    ("checkpoints/quartznet_finetuned.nemo", PretrainedFineTunedQuartzNet),
    ("checkpoints/quartznet_pretrained.nemo", PretrainedQuartzNet),
]

if __name__ == "__main__":
    results = {"results": []}

    # iterate through models, evaluate average WER over the train and test sets
    for checkpoint_path, model_class in models:
        model: Model = model_class(checkpoint_name=checkpoint_path)

        # eval over training set
        model.testing_setup("manifests/train_manifest.json")
        train_wer = model.test()

        # eval over testing set
        model.testing_setup("manifests/test_manifest.json")
        test_wer = model.test()

        results["results"].append(
            {
                "checkpoint_name": checkpoint_path.rsplit("/"),
                "train_wer": train_wer,
                "test_wer": test_wer,
            }
        )

    with open("results/dataset_eval.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(results, indent=1))
        f.write("\n")
