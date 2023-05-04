from convert import *
import torch

with torch.no_grad():
    onnx2pb("out/yolov2.onnx", "out/model.pb")