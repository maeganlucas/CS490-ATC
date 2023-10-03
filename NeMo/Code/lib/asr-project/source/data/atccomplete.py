import glob
import os
import re
import subprocess
from pathlib import Path
from typing import *

from data import Data, atccutils


class ATCCompleteData(Data):
    """
    This class defines the data format of the Air Traffic Control Complete dataset and provides functions
    for parsing the data into a common format for automatic data analysis (see ``Data``).

    This dataset is described in depth and can be obtained here: https://catalog.ldc.upenn.edu/LDC94S14A

    The following attributes are defined in this class due to the way the Air Traffic Control Complete
    dataset is formatted and distributed.
    """

    def __init__(self, data_root: str, **kwargs):
        """
        :param data_root: root path of the dataset (start point for parsing).
        :param kwargs: keyword arguments to pass to the super class.
        """
        super(ATCCompleteData, self).__init__(
            dataset_name="Air Traffic Control Complete", **kwargs
        )

        if not os.path.exists(data_root):
            raise FileNotFoundError(f"Could not find dataset root: '{data_root}'")

        # glob strings for audio and transcripts
        sphere_glob_string = os.path.join(data_root, "**/data/audio/*.sph")
        wav_glob_string = os.path.join(data_root, "**/data/audio/*.wav")
        transcript_glob_string = os.path.join(data_root, "**/data/transcripts/*.txt")

        # collect audio and transcript file, convert if needed
        sphere_files = glob.glob(sphere_glob_string, recursive=True)

        #: list of paths to audio files in the dataset.
        self._audio_glob = sorted(glob.glob(wav_glob_string, recursive=True))
        self._transcript_glob = sorted(
            glob.glob(transcript_glob_string, recursive=True)
        )

        if len(self._audio_glob) != len(self._transcript_glob):
            self.sphere_to_wav(sphere_files)
            self._audio_glob = sorted(glob.glob(wav_glob_string, recursive=True))
        """
        list of paths to transcript files that correspond to the audio
            files in the dataset. Transcripts are formatted as Lisp lists, each list corresponds
            to one sample in the data i.e. one transmission.
        """

        self.transcript_corrections: List[Tuple[str, str]] = [
            ("0h", "oh"),
            ("0r", "or"),
            ("8'll", "i'll"),
            ("kil0", "kilo"),
            ("altimeter;;;'s", "altimeter's"),
            ("bye]", "bye"),
            (" -", ""),
            (" 3 ", "three"),
            ("1347.85706", "one three four seven dot eight five seven zero six"),
            ("four]", "four"),
            # flight number metadata somehow made it into some of the transcripts
            ("swift61", ""),
            ("aal891", ""),
            # repeated words/hesitations
            ("ai", ""),
            ("cir-", ""),
            ("cli-", ""),
        ]
        """
        there are a lot of typos in this dataset; this is the running list with corrections
        list of (typo, correction) pairs (tuples)
        """

    def parse_transcripts(self) -> List[Dict[str, Union[str, float]]]:
        """
        Parse data indices in transcript files into dictionary objects with required info to be compatible with NeMo's manifest format.

        :returns: A list of dictionary objects.
        """
        assert len(self._audio_glob) == len(
            self._transcript_glob
        ), f"Number of audio and transcript files do not match: {len(self._audio_glob)} and {len(self._transcript_glob)}, respectively."
        data = []

        sounds_like_tag = re.compile(r"(\[sounds like(?P<guess>[A-Za-z\s\d]+)\]*)")
        annotation = re.compile(r"(\[[A-Za-z\s]+\])")

        for audio_path, transcript_path in zip(self._audio_glob, self._transcript_glob):
            # parse transcript file (returns a list of dictionary objects where each
            # object corresponds to each Lisp list in the transcript file)
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcript_data = atccutils.parse(f.readlines())

            # filter out tape-header, tape-tail, and comment blocks (and any other
            # extraneous info that could cause KeyErrors)
            for datum in transcript_data:
                if "TEXT" in datum.keys():
                    text: str = datum["TEXT"].lower()
                    # line breaks
                    text = "\n".join([t.strip() for t in text.split("//")])
                    text = "\n".join([t.strip() for t in text.split("/")])

                    # transcriber guesses
                    sounds_like_match = sounds_like_tag.match(text)
                    if sounds_like_match is not None:
                        text = sounds_like_match["guess"].strip()

                    # typos in transcripts
                    for typo, correction in self.transcript_corrections:
                        if typo in text:
                            text = text.replace(typo, correction)

                    # remove transcriber annotations
                    text = annotation.sub("", text)

                    if text.strip() != "":
                        duration = datum["TIMES"]["end"] - datum["TIMES"]["start"]

                        if duration < 1.0:
                            # print(f"File: {audio_path}\nText: {text}")
                            continue

                        data.append(
                            {
                                "audio_filepath": audio_path,
                                "text": text,
                                "offset": datum["TIMES"]["start"],
                                "duration": duration,
                            }
                        )

        # save manifest data to class attribute before returning
        self.data = data
        return data

    def sphere_to_wav(self, sphere_glob: List[str]) -> List[str]:
        """
        Runs ffmpeg on each sphere file in `sphere_glob` to convert the
        files from the NIST Sphere format to the MS Wav format. Also resamples
        the audio to 16k.

        :param sphere_glob: List of paths (strings) to sphere files to convert
        :returns: List of converted files
        """
        assert len(sphere_glob) > 0
        converted_paths = []

        for sphere_file in sphere_glob:
            sphere_file = Path(sphere_file)
            converted_file = str(sphere_file).replace(".sph", ".wav")
            if sphere_file.exists():
                # program and arguments to run to reformat/resample the sphere file
                process = [
                    "sox",
                    f"{sphere_file}",
                    "-r",
                    "16000",
                    f"{converted_file}",
                ]
                # for debugging
                # print(" ".join(ffmpeg_options))
                subprocess.run(process)
                converted_paths.append(converted_file)

        return converted_paths
