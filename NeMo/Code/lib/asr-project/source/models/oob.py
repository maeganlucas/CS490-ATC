"""
TODO: module description
"""
from typing import *

from models import Model
from nemo.collections.asr.models import EncDecCTCModel
from omegaconf import DictConfig


class RandomInitCTC(Model):
    def __init__(self, checkpoint_name: str = "none"):
        """
        :param checkpoint_name: checkpoint to load from and/or store to
        """
        #: model configuration (see NeMo model configuration files)
        self._config = self.load_config(config_path="config/config.yaml")
        self._config["model"]["train_ds"][
            "manifest_filepath"
        ] = "manifests/train_manifest.json"
        self._config["model"]["validation_ds"][
            "manifest_filepath"
        ] = "manifests/validation_manifest.json"

        self._model = EncDecCTCModel(cfg=DictConfig(self._config["model"]))

        super(RandomInitCTC, self).__init__(checkpoint_name)
