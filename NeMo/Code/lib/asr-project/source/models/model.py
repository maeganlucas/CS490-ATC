import gc
import logging
import os
from typing import *

import pytorch_lightning as pl
import torch
import yaml
from pytorch_lightning.callbacks import EarlyStopping
from nemo.collections.asr.models import EncDecCTCModel
from omegaconf import DictConfig
from tqdm import tqdm

logger = logging.getLogger(__name__)

test_config = {
    # this field must be updated by the setup method
    "manifest_filepath": None,
    "sample_rate": 16000,
    "labels": [
        " ",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "'",
    ],
    "batch_size": 8,
    "shuffle": False,
    "num_workers": 8,
    "pin_memory": True,
}

validation_stop_callback = EarlyStopping(monitor="val_wer", min_delta=0.05)


class Model(object):
    """
    Wrapper class for automating training and comparing multiple models. Will also help keep things consistent if different APIs/frameworks are used.
    """

    def __init__(self, checkpoint_path: str = "none", model_class=EncDecCTCModel):
        """
        :param checkpoint_path: path of the model checkpoint (these can be used interchangebly), defaults to ``"none"``.
        :param model_class: base class of the model for loading/restoring/saving to and from checkpoints, defaults to ``EncDecCTCModel``.
        """
        if checkpoint_path == "none":
            logger.warning("Model name has been left to default.")

        self.checkpoint_name = checkpoint_path
        if os.path.exists(self.checkpoint_name):
            self._model = model_class.restore_from(self.checkpoint_name)
            """
            PyTorch-based model architecture. This is the actual model that is trained and used for inference.
            Everything outside of this is a wrapper for ease of use.
            """
        else:
            self._model = None

    def load_config(self, config_path: str) -> Dict:
        """
        Loads the model config file from the specified path.

        :param config_path: Path (relative or absolute) to the config file.
        :returns: Resulting dictionary (from loading YAML file) as
            an ``omegaconf.DictCOnfig`` object.
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Configuration file path '{config_path}' does not exist"
            )

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.load(stream=f)

        return config

    def training_setup(
        self,
        training_manifest_path: str,
        validation_manifest_path: str = None,
        **trainer_args,
    ):
        """
        Checks for valid manifest paths and sets up data loaders for the training,
        testing, and validation datasets.

        Sets up a pytorch lightning trainer.

        :param training_manifest_path: Path to the training manifest
        :param testing_manifest_path: Path to the testing manifest
        :param validation_manifest_path: Path to the validation manifest
        :param trainer_args: keyword arguments for the pytorch lightning ``Trainer``
        """
        assert self._config is not None
        if not os.path.exists(training_manifest_path):
            raise FileNotFoundError(
                f"Training manifest path '{training_manifest_path}' does not exist"
            )
        if validation_manifest_path is not None:
            if not os.path.exists(validation_manifest_path):
                raise FileNotFoundError(
                    f"Validation manifest path '{validation_manifest_path}' does not exist"
                )

        # specify manifest paths
        self._config["model"]["train_ds"]["manifest_filepath"] = training_manifest_path
        self._config["model"]["train_ds"]["sample_rate"] = 16000
        self._config["model"]["train_ds"]["batch_size"] = 16
        self._config["model"]["train_ds"]["num_workers"] = os.cpu_count()

        if validation_manifest_path is not None:
            self._config["model"]["validation_ds"][
                "manifest_filepath"
            ] = validation_manifest_path

        # set up data partitions
        self._model.setup_training_data(DictConfig(self._config["model"]["train_ds"]))

        if validation_manifest_path is not None:
            self._model.setup_validation_data(
                DictConfig(self._config["model"]["validation_ds"])
            )

        # initialize lightning trainer
        self._trainer = pl.Trainer(**trainer_args)

    def testing_setup(self, test_manifest_path: str):
        """
        Loads and sets up the testing data for the model.

        :param test_manifest_path: path to the testing manifest data.
        """
        if not os.path.exists(test_manifest_path):
            raise FileNotFoundError(
                f"Test manifest path '{test_manifest_path}' does not exist"
            )

        # set manifest path
        test_config["manifest_filepath"] = test_manifest_path

        # set up test data partition
        self._model.setup_test_data(DictConfig(test_config))

    def fit(self) -> None:
        """
        Start the training process (for a NeMo model).
        """
        self._trainer.fit(self._model)

        os.makedirs("checkpoints", exist_ok=True)
        self._model.save_to(os.path.join("checkpoints", self.checkpoint_name))

    def test(
        self,
        testing_set: Union[Literal["train"], Literal["test"]] = "test",
        log_prediction: bool = False,
    ) -> float:
        """
        Tests the model and finds the average word error rate (WER) over test samples.

        :param testing_set: the dataset on which to test the model; can be either
            ``'train'`` or ``'test'``. Defaults to ``'test'``.
        :returns: The average WER over the test set (set specified by ``testing_set``).
        """
        if testing_set == "test":
            dataloader = self._model.test_dataloader
        elif testing_set == "train":
            dataloader = self._model.train_dataloader
        else:
            raise ValueError(
                f"argument 'testing_set' must take a value of either 'train' or 'test' got '{testing_set}' instead"
            )
        # log test predictions if set
        self._model._wer.log_prediction = log_prediction
        self._model.cuda()
        self._model.eval()
        # word error rate is defined as:
        # (substitutions + deletions + insertions) / number of words in label
        # i.e. (S+D+I) / N
        # S + D + I
        all_nums = []
        # N
        all_denoms = []

        # loop through test samples/batches and calculate individual WERs
        print(
            f"Evaluating performance on '{testing_set}' set ('{self.checkpoint_name}')"
        )
        for test_batch in tqdm(dataloader(), desc="Eval progress"):
            # test batches are made up of the following:
            # [signal, signal length, target, target length]
            test_batch = [x.cuda() for x in test_batch]

            # get model predictions for test samples (don't care about any other
            # returned values at this point in time)
            _, _, predictions = self._model(
                input_signal=test_batch[0], input_signal_length=test_batch[1]
            )

            # calculate WER for this batch of predictions
            self._model._wer.update(
                predictions=predictions,
                targets=test_batch[2],
                target_lengths=test_batch[3],
            )

            # get WER from module (returns average, numerators, and denominators)
            _, nums, denoms = self._model._wer.compute()
            self._model._wer.reset()

            all_nums.append(nums.cpu().numpy())
            all_denoms.append(denoms.cpu().numpy())

            # clean up memory for next batch
            del test_batch, predictions, nums, denoms
            gc.collect()
            torch.cuda.empty_cache()

        # return average over the dataset
        return sum(all_nums) / sum(all_denoms)

    @property
    def name(self) -> str:
        """
        The name of the model aka model checkpoint.
        """
        return self.checkpoint_name
