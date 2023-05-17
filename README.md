# ARTI
ARTI, an Augmented Reality Translation Interface.

## Warning
You will need an AssemblyAI token. This is a paid service. You can get a token at their website https://www.assemblyai.com.

## Installation

### Installing PyThorch with support for CUDA
This is optional, but it is necesary if you want ARTI to un on real-time.

You need a CUDA 11.8 supported GPU, you can check the supported GPUs in this table,
https://en.wikipedia.org/wiki/CUDA#GPUs_supported

First, download and install CUDA Toolkit 11.8.0
https://developer.nvidia.com/cuda-11-8-0-download-archive

Then, install PyTorch for CUDA 11.8

On Linux
```pip3 install numpy --pre torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/nightly/cu118```

On Windows
```pip install numpy --pre torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/nightly/cu118```

### Installing requirements
To install the required libraries, run

On Linux
```pip3 install -r requirements.txt```

On Windows
```pip install -r requirements.txt```

### Running ARTI
To start the application, run

On Linux
```python3 ./arti.py```

On Windows
```python ./arti.py```

### Changing translation language and input devices
To change the language, modify the variable `LANGUAGE` in `arti.py`

To change the input devices, change the variables `AUDIO_INPUT` and `VIDEO_INPUT` in `arti.py`. The default values are `AUDIO_INPUT = 1` and `VIDEO_INPUT = 0`, and refer to the built in microphone and camera.