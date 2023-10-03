import nemo.collections.asr as nemo_asr
import torch
from typing import *
import numpy as np
from nemo.collections.asr.parts.preprocessing.segment import AudioSegment


class Transcribe_ATC:
    def __init__(self):
        # EncDecCTCModelBPE is for citrinet models you will need to change this depending
        # on the model we are using
        # EncDecCTCModel is for quartznet and jasper
        self.model_check_point = "ft100epoch_stt_en_citrinet_512_tokenizer.nemo"
        try:
            self.base_model = nemo_asr.models.EncDecCTCModelBPE.restore_from(
                self.model_check_point
            )
        except:
            self.base_model = nemo_asr.models.EncDecCTCModel.restore_from(
                self.model_check_point
            )

        # save model states/values
        self.model_state = self.base_model.training
        self.dither_value = self.base_model.preprocessor.featurizer.dither
        self.pad_value = self.base_model.preprocessor.featurizer.pad_to

        # eliminate intentional randomness in preprocessing
        self.base_model.preprocessor.featurizer.dither = 0.0
        self.base_model.preprocessor.featurizer.pad_to = 0

        # inference setup: put model in evaluation mode, freeze encoder/decoder
        self.base_model.eval()
        self.base_model.encoder.freeze()
        self.base_model.decoder.freeze()

    def transcribe_audio(self, file_name):
        files = [file_name]
        return self.base_model.transcribe(paths2audio_files=files, batch_size=1)[0]

    @torch.no_grad()
    def transcribe_audio_array(
        self,
        signal,
        duration: float = 0.0,
        offset: float = 0.0,
        device: Union[Literal["cuda"], Literal["cpu"]] = "cuda",
    ):
        self.base_model.to(device)

        # get input data and length
        # signal = AudioSegment.from_file(
        #     path, 16000, offset=offset, duration=duration
        # ).samples

        # get model predictions/logits
        logits, logits_length, predictions = self.base_model.forward(
            input_signal=torch.tensor(np.array([signal])).to(device),
            input_signal_length=torch.tensor([signal.shape[0]]).long().to(device),
        )

        prediction, _ = self.base_model.decoding.ctc_decoder_predictions_tensor(
            logits, logits_length
        )

        # reset model states/preprocessor values
        self.base_model.train(mode=self.model_state)
        self.base_model.preprocessor.featurizer.dither = self.dither_value
        self.base_model.preprocessor.featurizer.pad_to = self.ad_value

        return prediction[0]
