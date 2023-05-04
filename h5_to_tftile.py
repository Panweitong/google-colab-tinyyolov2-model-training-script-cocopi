from convert import *
import torch

with torch.no_grad():
    h5_to_tftile("out/model.h5", "out/yolov2_h5.tflite")