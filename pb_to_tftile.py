from convert import *
import torch

with torch.no_grad():
    pb_to_tftile("out/model.pb", "out/yolov2_pb.tflite")