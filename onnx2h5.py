from convert import *
import torch

with torch.no_grad():
    onnx2h5("out/yolov2.onnx", "out/model.h5")