import glob
import os
import re
from typing import *
from xml.etree import ElementTree

import librosa
from data import Data


class ATCO2SimData(Data):
    """
    This class defines the format for the Air Traffic Control 2 dataset and implements
    functions to parse the data into a common format for data analysis.

    This dataset is described in more depth and can be obtained here: https://www.atco2.org/data

    See readme.txt in the root of the dataset for full description of data, including
    audio and transcription formats. Notes on the transcript format can be found in
    ``parse_transcripts``.
    """

    def __init__(self, data_root: str, **kwargs):
        """

        """
        super(ATCO2SimData, self).__init__(dataset_name="ATCO2", **kwargs)
        transcript_glob_string = os.path.join(data_root, "DATA/*.xml")
        audio_glob_string = os.path.join(data_root, "DATA/*.wav")

        #: Collection of transcripts file paths in the dataset
        self._transcript_glob = sorted(glob.glob(transcript_glob_string))
        #: Collection of audio file paths in the dataset
        self._audio_glob = sorted(glob.glob(audio_glob_string))

        #: Typo correction pairs. Tuples of two strings; left is the typo, right is the correction.
        self.transcription_corrections = [
            ("your're", "you're"),
            ("affirmatif", "affirmative"),
            ("zurrich", "zurich"),
        ]

        assert len(self._transcript_glob) != 0
        assert len(self._audio_glob) != 0

    def parse_transcripts(self) -> List[Dict[str, Union[str, float]]]:
        """
        Data is labeled in an XML hierarchy. ``<data>`` is the root node which is made up
        of ``<segments>`` which contain the following:

        * start/end times -- ``<start>`` and ``<end>``, respectively

        * speaker ID -- ``<speaker>``

        * speaker label -- ``<speaker_label>``

        * transcription -- ``<text>``

        * tags:

            * ``<correct_transcript>`` -- do not use data instance if set to ``0``

            * ``<correct_tagging>`` -- do not use word tagging if set to ``0``

            * ``<non_english>`` -- do not use data instance if set to ``1``

        Transcription manual with full description here: https://www.spokendata.com/atco2/annotation-manual
        """
        assert len(self._audio_glob) == len(
            self._transcript_glob
        ), f"Number of audio and transcript files do not match: {len(self._audio_glob)} and {len(self._transcript_glob)}, respectively."
        data = []

        # two main groups of open/closing pairs
        # TODO: cut this down; this pattern does not need to be this long
        annotation_tag = re.compile(
            # begins with '#'
            r"(\[#[A-Za-z\-\\\s]+\]|"
            r"\[/#[A-Za-z\-\\\s]+\]|"
            # does not begin with '#'
            r"\[[A-Za-z\-\\\s]+\]|"
            r"\[/[A-Za-z\-\\\s]+\])|"
        )

        # each pattern has two closures for substitution operation later
        prefixes = re.compile(r"(\([A-Za-z]+\-\))")
        suffixes = re.compile(r"(\(\-[A-Za-z]+\))")

        non_english_tag = re.compile(r"(\[[#]NE\s\])")

        for audio_path, transcript_path in zip(self._audio_glob, self._transcript_glob):
            # get the root data element
            transcript_root = ElementTree.parse(transcript_path).getroot()
            # iterate on child nodes (should be made up of <segment> tags only)
            segment_nodes = transcript_root.findall("segment")
            assert segment_nodes is not None

            # iterate through all segments and extract "<text>" tags
            for segment in segment_nodes:
                tag_nodes = segment.find("tags")
                assert tag_nodes is not None

                # check for validity tags (correct_transcript, non_english)
                correct_transcript = tag_nodes.find("correct_transcript")
                non_english = tag_nodes.find("non_english")
                # skip/exclude the sample is the transcript metadata tells us to
                if correct_transcript is not None and correct_transcript.text == "0":
                    continue
                if non_english is not None and non_english.text == "1":
                    continue

                # get and process text
                for text_node in segment.iterfind("text"):
                    assert text_node is not None
                    # fetch text from the xml tag
                    text = text_node.text.lower()
                    # skip unlabeled non-english transcripts
                    if non_english_tag.match(text) is not None:
                        continue
                    # remove transcript annotations
                    text = annotation_tag.sub("", text)

                    # this is annoying just bear with me:
                    # -----------------------------------
                    # match the pattern to the text (find the pattern in the
                    # string that matches the named closure, if it exists)
                    # substitute the matched word for the match pattern
                    # i.e. replace change(-ed) with changed
                    for match in suffixes.finditer(text):
                        text = suffixes.sub("", text)

                    # same as above just with prefixes instead of suffixes
                    for match in prefixes.finditer(text):
                        text = prefixes.sub("", text)
                    # -----------------------------------
                    # /annoyance

                    for typo, correction in self.transcription_corrections:
                        text = text.replace(typo, correction)

                    text = text.strip()

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
