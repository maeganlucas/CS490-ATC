# Environment Installation and Setup

## Conda Setup
```bash
conda create -n nemo python=3.8
conda activate nemo
```

## PyTorch and Cuda
Double-check the [PyTorch Getting Started page](https://pytorch.org/get-started/locally/) to make sure the most up-to-date version is installed:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

## NeMo Dependencies
Double-check [NeMo's readme](https://github.com/NVIDIA/NeMo) to make sure all required dependencies are installed.

Debian-based systems (e.g. Ubuntu, Debian, etc.):
```bash
sudo apt-get update && sudo apt-get install -y libsndfile1 ffmpeg
```

RPM-based systems (e.g. RHEL, Fedora, CentOS, etc.; may require [RPM Fusion to be setup](https://rpmfusion.org/Configuration#Command_Line_Setup_using_rpm)):
```bash
sudo dnf install -y libsndfile ffmpeg
```

All systems, after installing `libsndfile` and `ffmpeg`:
```bash
pip install Cython
pip install nemo_toolkit[all]
```
**Note**: Depending on terminal/shell `nemo_toolkit` may need to be escaped as one of the following:
* `nemo_toolkit['all']`
* `nemo_toolkit\[all\]`
* `"nemo_toolkit[all]"`