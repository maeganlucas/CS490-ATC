import json
import logging
import os
from pathlib import Path
from typing import *

import librosa
import librosa.display
import matplotlib
import matplotlib.collections
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)

manifest_fields: List[str] = ["audio_filepath", "duration", "text"]


class Data:
    """Top level Data class that provides several methods for processing and analyzing text datasets for NLP processes."""

    def __init__(self, random_seed: int = None, dataset_name: str = "data"):
        """
        :param random_seed: value to seed numpy random with.
        :param dataset_name: Name of the dataset.
        """
        #: Dataset name, defaults to ``"data"``
        self.dataset_name = dataset_name
        self.data = []
        """
        list of dictionary objects. Each object corresponds to one data sample and typically contains the following metadata:

            * ``audio_filepath`` (**required**) - path to the audio data (input data). Type: ``str``, absolute file path, conforms to ``os.PathLike``

            * ``duration`` (**required**) - duration, in seconds, of the audio data. Type: ``float``

            * ``text`` (**required**) - transcript of the audio data (label/ground truth). Type: ``str``

            * ``offset`` - if more than one sample is present in a single audio file, this field specifies its offset i.e. start time in the audio file. Type: ``float``
        """

        #: create random number generator sequence with specified seed, if applicable
        self._random = np.random.default_rng(random_seed)
        self.normalized = False

    def parse_transcripts(self) -> List[str]:
        """
        This method must be overridden and implemented for each implementation of this class for datasets.

        :returns: Dictionary (from `json` module) with necessary data info e.g. annotations, file
            path, audio length, offset.
        """
        raise NotImplementedError(
            "This is an abstract method that should be implemented and overridden for "
            "all classes that implement this one. If this method has been called, there "
            "is an issue with the class that extended the Data class."
        )

    def create_token_hist(
        self, token_counts: List[int] = [],
    ) -> matplotlib.figure.Figure:
        """
        Calculates the number of utterances in each sample and generates a histogram.

        Utterance counts are determined by splitting each transcript on whitespace and
        calculating the length of the resulting list.

        :param utterance_counts: (optional) `list` of `ints` for precalculated utterance counts.
        :returns: a `matplotlib.pyplot.Figure` object aka final plot. Use plt.show() to render the plot.
        """
        # Clear figure and axes
        plt.clf(), plt.cla()
        # check if manifest data has been generated, parse transcripts and generate
        # manifest data if not
        if len(self.data) == 0:
            self.parse_transcripts()

        # check if utterance counts (optional arg) has been provided, calculate utterance
        # counts from transcriptions
        if len(token_counts) == 0:
            for data in self.data:
                data = data["text"]
                words = data.split(" ")
                token_counts.append(len(words))

        histogram = plt.hist(token_counts)
        plt.xlabel("Bins")
        plt.ylabel("Token Counts")
        plt.title(f"Tokens per Sample in {self.name}")

        return histogram

    def token_freq_analysis(
        self, normalize: bool = False
    ) -> Dict[str, Union[int, List]]:
        """
        Perform a token frequency analysis on the dataset (number of occurrences of each token throughout the dataset).

        :param normalize: (optional) whether to normalize values such that all frequencies add to 1.
        :returns: ``dict`` with tokens and number of occurrences of those tokens throughout the dataset.

        If ``normalize`` is set to ``True`` a dictionary with tokens corresponding to a list is returned e.g.
        ::

            {
                "token": [24, 0.0486]
            }

        """
        if len(self.data) == 0:
            self.parse_transcripts()

        # tokens corresponding to occurences/frequencies
        token_freqs = {}

        for sample in self.data:
            sample = sample["text"]
            for token in sample.split():
                if token in token_freqs.keys():
                    # increment occurences if there is already an entry
                    token_freqs[token] += 1
                else:
                    # add entry if one does not exist already
                    token_freqs[token] = 1

        if normalize:
            # convert from token occureces to frequencies: (# of token occurences / # of tokens)
            num_tokens = len(token_freqs)
            for token, freq in token_freqs.items():
                token_freqs[token] = [freq, float(freq) / num_tokens]

        return token_freqs

    def dump_manifest(
        self, outfile: str, make_dirs: bool = True, return_list: bool = False
    ) -> Union[None, List[Dict]]:
        """
        Dump input data paths, labels, and metadata to `outfile` in NeMo manifest format.

        :param outfile: output path.
        :param make_dirs: (optional) whether to make nonexistent parent directories in ``outfile``. Defaults to ``True``.
        :param return_list: Whether to return a list of strings instead of creating and dumping to a file.
        :returns: Either ``None`` or a list of strings according to ``return_list``.
        """
        outfile = Path(outfile).absolute()
        os.makedirs(str(outfile.parent), exist_ok=make_dirs)

        # check if manifest data has been generated
        if len(self.data) == 0:
            self.parse_transcripts()

        # write each data point its own line in the file, in json format (conform to NeMo
        # manifest specification)
        with open(str(outfile), "w") as manifest:
            for entry in self.data:
                manifest.write(json.dumps(entry))
                manifest.write("\n")

        if return_list:
            return self.data

    def concat(self, child_dataset: "Data"):
        """
        Concatenates data classes/sets. Extends the data array of parent object to
        include data from child object. Also updates any relevant common metadata
        fields.

        :param child_dataset: Dataset to concatenate into this object.
        """
        self.data.extend(child_dataset.data)
        self.dataset_name = f"{self.name} + {child_dataset.name}"

    def generate_spec(
        self, index_or_path: Union[int, str, None] = None
    ) -> Union[str, Tuple[str, str]]:
        """
        Generate a Mel-scale spectrogram from the index (in the data list
        attribute) or provided file path. If neither index or path is provided,
        a sample will be chosen at random.

        :param index_or_path: either a file path or an index in the data list (``self.data``)
        :returns: Either the path to the audio file or a Tuple of the audio file path and transcription.
        """
        # if an offset is relevant, set this to the correct value
        offset = 0
        # there is a realistic chance that this variable won't be created, so
        # it has to be initialized here first
        duration = 0
        transcript = ""
        # if a value is given, use either the index or path
        if index_or_path is not None:
            if isinstance(index_or_path, int):
                sample = self.data[index_or_path]
                audio_file = sample["audio_filepath"]
                transcript = sample["text"]

                if "offset" in sample:
                    offset = sample["offset"]
                    duration = sample["duration"]
            elif isinstance(index_or_path, str):
                audio_file = index_or_path
        # otherwise pick a sample at random
        else:
            random_index = int(len(self.data) * self._random.random())
            sample = self.data[random_index]
            audio_file = sample["audio_filepath"]
            transcript = sample["text"]

            # for files with multiple samples in them, this indicates the time
            # at which THIS sample begins. Use with duration to get entire sample
            if "offset" in sample:
                offset = sample["offset"]
                duration = sample["duration"]

        # if the duration wasn't set above, set it here
        if duration == 0:
            duration = librosa.get_duration(filename=audio_file)

        # load audio data and generate spectrogram
        data, sample_rate = librosa.load(audio_file, offset=offset, duration=duration)
        melspec_data = librosa.feature.melspectrogram(y=data, sr=sample_rate)
        melspec_data = librosa.power_to_db(melspec_data, ref=np.max)

        # add spec data to plot
        fig, ax = plt.subplots()
        img = librosa.display.specshow(
            melspec_data, x_axis="time", y_axis="mel", sr=sample_rate, ax=ax
        )
        fig.colorbar(img, ax=ax, format="%+2.0f dB")

        # return both path and transcript if available, otherwise just the path
        return {
            "file": audio_file,
            "transcript": transcript,
            "offset": offset,
            "duration": duration,
        }

    def shuffle(self) -> None:
        """
        Wrapper function for np.random.shuffle
        """
        self._random.shuffle(self.data)

    @property
    def name(self) -> str:
        """
        :returns: The name of this dataset
        """
        return self.dataset_name

    @property
    def num_samples(self) -> int:
        """
        :returns: The number of samples in this dataset
        """
        return len(self.data)

    @property
    def duration(self) -> float:
        """
        :returns: The cumulative duration of the data (in seconds).
        """
        total_hours = 0
        for item in self.data:
            total_hours += item["duration"]
        return total_hours

    @property
    def total_tokens(self) -> int:
        """
        :returns: The total number of tokens in the transcripts of the dataset (labels).
        """
        num_tokens = 0
        for item in self.data:
            tokens = item["text"].split(" ")
            num_tokens += len(tokens)
        return num_tokens

    @property
    def unique_tokens(self) -> int:
        """
        :returns: The number of unique tokens in the dataset. Repeating tokens are removed from this total.
        """
        unique_tokens = []
        for item in self.data:
            tokens = item["text"].split(" ")
            for token in tokens:
                if token not in unique_tokens:
                    unique_tokens.append(token)
        return len(unique_tokens)

    @classmethod
    def from_manifest(cls: "Data", manifest_path: str, random_seed: int = 1) -> "Data":
        """
        Loads dataset info from a manifest file (if dataset has already been
        parsed into the NeMo manifest format). `parse_transcripts` does not need
        to be called after this function.

        **Use with caution**: If the manifest files were generated on another system,
        it is highly likely that the file paths in the manifest are incorrect and will
        result it every other function/method to break or behave strangely.

        :param manifest_path: path to the manifest file
        :param random_seed: random seed to initialize the class with (defaults to 1)
        :returns: a data class initialized with the data in the manifest file
        """
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest path not found '{manifest_path}'")

        # initialize class
        data = cls(random_seed=random_seed)

        # extract manifest info
        with open(manifest_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line_data = json.loads(line)

                # check if minimum required fields are present:
                for field in manifest_fields:
                    if field not in line_data.keys():
                        logger.warn(f"Required field not found: '{field}'")

                # warnings about non-existent file paths
                if "audio_filepath" in line_data.keys():
                    if not os.path.exists(line_data["audio_filepath"]):
                        logger.warn(
                            f"Audio path not found: '{line_data['audio_filepath']}'"
                        )

                # append sample info to object
                data.data.append(line_data)

        return data

    @classmethod
    def from_iterable(cls: "Data", iterable: Iterable, random_seed: int = 1) -> "Data":
        """
        TODO
        """
        instance = cls(random_seed=random_seed)

        if not isinstance(iterable, list):
            instance.data = []
            for item in iterable:
                instance.data.append(item)
        else:
            instance.data = iterable

        return instance


def split_data(
    data: Data,
    test: bool = True,
    validation: bool = True,
    validation_split_ratio: float = 0.1,
    test_split_ratio: float = 0.2,
    shuffle: bool = True,
) -> Union[Tuple[Data, Data], Tuple[Data, Data, Data]]:
    """
    TODO
    :param data:
    :param test:
    :param validation:
    :param validation_split:
    :param test_split:
    :returns:
    """
    assert data is not None
    assert data.data is not None
    assert len(data.data) != 0

    data_length = len(data.data)
    train_size = data_length

    if test:
        test_size = int(data_length * test_split_ratio)
        train_size = data_length - test_size

    if validation:
        validation_size = int(train_size * validation_split_ratio)
        train_size -= validation_size

    train_data = data.data[:train_size]

    if test:
        test_data = data.data[train_size:]

    if validation:
        validation_data = train_data[:validation_size]
        train_data = train_data[validation_size:]

    train_data = Data.from_iterable(train_data)

    if test:
        test_data = Data.from_iterable(test_data)

    if validation:
        validation_data = Data.from_iterable(validation_data)

    data_splits = [train_data]

    if test:
        data_splits.append(test_data)
    if validation:
        data_splits.append(validation_data)

    return tuple(data_splits)

