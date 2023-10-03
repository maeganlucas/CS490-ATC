import pandas as pd
import os
import json
import string

import editdistance
from nemo.collections.asr.metrics.wer import word_error_rate
from models import PretrainedFineTunedJasper
from utils import transcribe_audio

audio_transcript_mappings = [
    (
        "/home/students/vandebra/programming/pilot_vr_training/15-1- Ormond Departure to Daytona Arrival_Part 1.mp3",
        "/home/students/vandebra/programming/pilot_vr_training/15-2-Ormond_Departure_to_Daytona_Arrival_1.xlsx",
    ),
    (
        "/home/students/vandebra/programming/pilot_vr_training/15-1- Ormond Departure to Daytona Arrival_Part 2.mp3",
        "/home/students/vandebra/programming/pilot_vr_training/15-2-Ormond_Departure_to_Daytona_Arrival_2.xlsx",
    ),
    (
        "/home/students/vandebra/programming/pilot_vr_training/15-1- Ormond Departure to Daytona Arrival_Part 3.mp3",
        "/home/students/vandebra/programming/pilot_vr_training/15-2-Ormond_Departure_to_Daytona_Arrival_3.xlsx",
    ),
]


def preprocess_transcript(text: str) -> str:
    """
    Args:
        `text`: transcript/string to preprocess

    Returns:
        processed text
    """
    text = text.lower()
    # replace windows smart quote
    text = text.replace("\u2019", "'")
    text = text.replace("-", " ")

    for c in string.punctuation:
        text = text.replace(c, "")

    return text.strip()


if __name__ == "__main__":
    # manifest format (json)
    test_data_points = []

    model = PretrainedFineTunedJasper(
        checkpoint_path="checkpoints/jasper_finetuned.nemo"
    )

    for audio_path, transcript_path in audio_transcript_mappings:
        # sanity checks
        assert os.path.exists(audio_path)
        assert os.path.exists(transcript_path)

        frame = pd.read_excel(
            transcript_path,
            usecols=["transcript", "start_time", "end_time", "duration"],
        )

        for row in frame.itertuples():
            processed_transcript = preprocess_transcript(row.transcript)
            prediction = transcribe_audio(
                path=audio_path,
                model=model,
                duration=row.duration,
                offset=row.start_time,
            )

            sample_wer = word_error_rate(
                hypotheses=[prediction], references=[processed_transcript]
            )

            test_data_points.append(
                {
                    "audio_filepath": audio_path,
                    "text": processed_transcript,
                    "duration": round(row.duration, 2),
                    "offset": round(row.start_time, 2),
                    "prediction": prediction,
                    "wer": sample_wer,
                }
            )

    with open("manifests/pilot_vr.json", "w", encoding="utf-8") as f:
        f.write("\n".join([json.dumps(data_point) for data_point in test_data_points]))

    print(f"Total number of samples: {len(test_data_points)}")
    print(
        f"Total duration of samples: {sum([data['duration'] for data in test_data_points])}"
    )
    print(
        f"Average WER: {word_error_rate([data['prediction'] for data in test_data_points], [data['text'] for data in test_data_points])}"
    )

    reformated_data = {
        "text": [],
        "prediction": [],
        "wer": [],
        "offset": [],
        "duration": [],
        "audio_filepath": [],
    }

    for key in reformated_data.keys():
        for data in test_data_points:
            reformated_data[key].append(data[key])

    frame = pd.DataFrame({k: v for k, v in reformated_data.items()})
    frame.to_excel("pilot_vr_prediction.xlsx")
