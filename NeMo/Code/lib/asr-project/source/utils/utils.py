import torch
import os
import numpy as np
from models import Model
from nemo.collections.asr.parts.preprocessing.segment import AudioSegment
from typing import *


# TODO wrapper functions in `Model` to help make this a bit nicer
@torch.no_grad()
def transcribe_audio(
    path: str,
    model: Model,
    duration: float = 0.0,
    offset: float = 0.0,
    device: Union[Literal["cuda"], Literal["cpu"]] = "cuda",
) -> str:
    """
    Transcribe the audio in ``path`` with an optional offset and duration in case there is more than one
    data sample in the file.

    Use this function if the ``transcribe`` method provided by NeMo ASR classes does not does not fit the
    use case.

    :param path: path to the audio file to transcribe (or file with the sample(s))
    :param model: model to use to transcribe the audio. This should be an instance of ``models.Model``
    :param duration: (optional) duration, in seconds, of the file or the sample in the file (in this case,
        ``offset`` needs to be specified as well). If this is unspecified the length of the audio file will
        be used instead (i.e. samples / sample_rate).
    :param offset: (optional) offset, in seconds, to the start of the sample. In other words, the start time,
        in seconds, of the sample.
    :param device: (optional) device/accelerator to use. Defaults to ``"cuda"``.
    :returns: Sequence of decoded model predictions for the given sample, as a ``str``. Simply put, the
        predicted transcription.
    """
    assert path is not None
    assert os.path.exists(path)
    assert model is not None

    # save model states/values
    model_state = model._model.training
    dither_value = model._model.preprocessor.featurizer.dither
    pad_value = model._model.preprocessor.featurizer.pad_to

    # eliminate intentional randomness in preprocessing
    model._model.preprocessor.featurizer.dither = 0.0
    model._model.preprocessor.featurizer.pad_to = 0

    # inference setup: put model in evaluation mode, freeze encoder/decoder
    model._model.eval()
    model._model.encoder.freeze()
    model._model.decoder.freeze()

    model._model.to(device)

    # get input data and length
    signal = AudioSegment.from_file(
        path, 16000, offset=offset, duration=duration, channel_selector=0
    ).samples

    # get model predictions/logits
    logits, logits_length, predictions = model._model.forward(
        input_signal=torch.tensor(np.array([signal])).to(device),
        input_signal_length=torch.tensor([signal.shape[0]]).long().to(device),
    )

    prediction, _ = model._model.decoding.ctc_decoder_predictions_tensor(
        logits, logits_length
    )

    # reset model states/preprocessor values
    model._model.train(mode=model_state)
    model._model.preprocessor.featurizer.dither = dither_value
    model._model.preprocessor.featurizer.pad_to = pad_value

    return prediction[0]
