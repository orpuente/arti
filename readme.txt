OpenCV with CUDA support
https://machinelearningprojects.net/build-opencv-with-cuda-and-cudnn/

yolov7
https://www.youtube.com/watch?v=hYtaxXCtBJk

PyTorch for CUDA 11.8
pip3 install numpy --pre torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/nightly/cu118

On Windows
pip install numpy --pre torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/nightly/cu118


YOLOv7 on an image
python .\detect.py --weights .\yolov7.pt --conf 0.25 --img-size 640 --source .\inference\images\horses.jpg --device 0

YOLOv7 on webcam
python .\detect.py --weights .\yolov7.pt --conf 0.25 --img-size 640 --source 0 --device 0