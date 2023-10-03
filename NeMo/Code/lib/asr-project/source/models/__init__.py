import logging

import torch

from .model import Model, validation_stop_callback
from .jasper import PretrainedFineTunedJasper, PretrainedJasper
from .oob import RandomInitCTC
from .quartznet import PretrainedFineTunedQuartzNet, PretrainedQuartzNet

# from .contextnet import *
# from transformers import *

logger = logging.getLogger(__name__)

# hardware check
if not torch.cuda.is_available():
    logger.warning(f"GPU or TPU is not detected or not available")

__all__ = [
    "Model",
    "PretrainedFineTunedJasper",
    "PretrainedJasper",
    "RandomInitCTC",
    "PretrainedFineTunedQuartzNet",
    "PretrainedQuartzNet",
]
