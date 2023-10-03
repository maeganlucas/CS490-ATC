"""
The classes in this module implement three permutations of The Jasper ASR model. It
is a Deep Time-Delay Neural Network (TDNN) comprised of block of one-dimensional
convolutional layers.

All Jasper models contain B blocks and R sub-blocks. Each sub-block contains a
one-dimensional convolution, batch normalization, ReLU activation, and dropout.

This model was trained and tested on the LibriSpeech corpus (conversational english).
Pretrained model checkpoints are also trained/tested on the LibriSpeech dataset.

See class descriptions for implementation specific deviations.

References:
-----------
[0] https://arxiv.org/abs/1904.03288
"""
from typing import *

from models import Model
from nemo.collections.asr.models import EncDecCTCModel


class PretrainedJasper(Model):
    """
    This class instantiates a pretrained Jasper model (without fine-tuning on
    additional data) and tests it on the designated test data to obtain a
    baseline WER.

    Model name: ``"stt_en_jasper_10x5dr"``

    Tokenizer: ``None``
    """

    def __init__(
        self,
        pretrained_model_name: str = "stt_en_jasper10x5dr",
        checkpoint_name: str = "none",
    ):
        """
        :param pretrained_model_name: name of the pretrained model to download from NGC.
        :param checkpoint_name: name of the model checkpoint for loading/saving.
        """
        self._config = self.load_config(config_path="config/jasper_10x5dr.yaml")
        # call super constructor to finish initializing the object
        super(PretrainedJasper, self).__init__(checkpoint_name)
        if self._model is None:
            self._model = EncDecCTCModel.from_pretrained(pretrained_model_name)

    def fit(self):
        """
        Overriding since the goal of this class is just to establish a baseline WER
        before fine tuning or training from scratch
        """
        pass


class PretrainedFineTunedJasper(Model):
    def __init__(
        self,
        pretrained_model_name: str = "stt_en_jasper10x5dr",
        checkpoint_path: str = "none",
    ):
        """
        :param pretrained_model_name: name of the pretrained model to download from NGC.
        :param checkpoint_path: path to the model checkpoint for loading/saving.
        """
        # call super constructor to initialize the object
        self._config = self.load_config(config_path="config/jasper_10x5dr.yaml")
        super(PretrainedFineTunedJasper, self).__init__(checkpoint_path)
        if self._model is None:
            self._model = EncDecCTCModel.from_pretrained(pretrained_model_name)
