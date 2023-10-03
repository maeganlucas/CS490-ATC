import json
import os
from models import PretrainedFineTunedJasper
from utils import transcribe_audio


def filter_false_starts(return_list=False):
    false_start_markers = ["um", "ah", "er", "uh", "eh"]
    false_start_datapoints = []

    with open("manifests/all_manifest.json", "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = json.loads(line)

            for marker in false_start_markers:
                if marker in line["text"].split():
                    false_start_datapoints.append(line)

    with open("manifests/false_starts.json", "w", encoding="utf-8") as f:
        for datum in false_start_datapoints:
            f.write(json.dumps(datum))
            f.write("\n")

    return false_start_datapoints


if __name__ == "__main__":
    false_start_datapoints = []
    false_start_predictions = []

    if not os.path.exists("manifests/false_starts.json"):
        false_start_datapoints = filter_false_starts(return_list=True)

    model = PretrainedFineTunedJasper(
        checkpoint_path="checkpoints/jasper_finetuned.nemo"
    )

    assert len(false_start_datapoints) != 0
    for datum in false_start_datapoints:
        datum["prediction"] = transcribe_audio(
            path=datum["audio_filepath"],
            model=model,
            duration=datum["duration"],
            offset=datum["offset"] or 0.0,
            device="cuda",
        )
        false_start_predictions.append(datum)

    with open("manifests/false_start_predictions.json", "w", encoding="utf-8") as f:
        for datum in false_start_predictions:
            f.write(json.dumps(datum))
            f.write("\n")

