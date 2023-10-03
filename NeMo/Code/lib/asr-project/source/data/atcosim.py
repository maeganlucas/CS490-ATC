import glob
import os
import re
from typing import *

import librosa
from data import Data


class ATCOSimData(Data):
    """
    This class describes the format of the Air Traffic Control Simulation Corpus
    and defines functions for parsing the data into a common format for data analysis.

    This dataset is described in more depth and can be obtained here: https://www.spsc.tugraz.at/databases-and-tools/atcosim-air-traffic-control-simulation-speech-corpus.html

    The data is shipped in iso (disk) format. To extract, mount the disk onto the file system and copy the data
    into another directory.

    ::

        mount -t iso9660 -o loop atcosim.iso atcosimmount
        cp -r atcosimmount .
    """

    def __init__(self, data_root: str, **kwargs):
        """
        :param data_root: path to the root of the dataset.
        :param kwarg: keyword arguments to pass to the super class.
        """
        super(ATCOSimData, self).__init__(dataset_name="ATCO", **kwargs)
        # glob patterns for audio and transcripts
        transcript_glob_string = os.path.join(data_root, "txtdata/**/*.txt")
        audio_glob_string = os.path.join(data_root, "wavdata/**/*.wav")

        #: collection of paths to transcript files
        self._transcript_paths = sorted(
            glob.glob(transcript_glob_string, recursive=True)
        )

        #: collection of paths to audio files
        self._audio_paths = sorted(glob.glob(audio_glob_string, recursive=True))

        # at the moment this is easier than updating the regex to exclude this specific file
        wordlist_path = os.path.join(data_root, "txtdata/wordlist.txt")
        if os.path.exists(wordlist_path):
            self._transcript_paths.remove(wordlist_path)

        #: typo correction pairs; left is the typo, right is the corrected text
        self.transcription_corrections = [
            ("kil0", "kilo"),
            ("ai", "air"),
            ("airr", "air"),
        ]

    def parse_transcripts(self) -> List[Dict[str, Union[str, float]]]:
        """
        Parse data indices in transcript files into dictionary objects with required info to be compatible with NeMo's manifest format.

        :returns: A list of dictionary objects.
        """
        assert len(self._audio_paths) == len(
            self._transcript_paths
        ), f"Number of audio and transcript files do not match: {len(self.audio_glob)} and {len(self.transcript_glob)}, respectively."
        data = []

        # regular expressions for removing transcript annotations
        xml_tag = re.compile(r"(<[A-Z]+>|</[A-Z]+>)")
        annotation_tag = re.compile(r"(\[[A-Z]+\])")
        special_chars = re.compile(r"[=~@]")
        hesitation_tokens = re.compile(r"(ah|hm|ahm|yeah|aha|nah|ohh)")
        non_english_tags = re.compile(r"(<FL>.</FL>)")

        for audio_path, transcript_path in zip(
            self._audio_paths, self._transcript_paths
        ):
            # read data from file
            with open(transcript_path, "r") as f:
                text = "".join([t.strip() for t in f.readlines()])

            # skip non-english samples
            if non_english_tags.match(text):
                continue

            # remove transcript annotations
            text = xml_tag.sub("", text)
            text = annotation_tag.sub("", text)
            text = special_chars.sub("", text)
            text = hesitation_tokens.sub("", text)

            # lower case, remove whitespace
            text = text.lower().strip()

            # correct identified typos, see `transcription_crrections` for
            # the full list
            for typo, correction in self.transcription_corrections:
                if typo in text:
                    text = text.replace(typo, correction)

            # some transcripts are empty after removing transcriber
            # annotations
            if text != "":
                data.append(
                    {
                        "audio_filepath": audio_path,
                        "duration": librosa.get_duration(filename=audio_path),
                        "text": text,
                    }
                )

        self.data = data
        return data
