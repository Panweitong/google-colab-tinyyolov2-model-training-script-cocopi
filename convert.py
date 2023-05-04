import torch.onnx
import torch
import numpy as np

import onnx
from onnx_tf.backend import prepare
import os
from onnx2keras import onnx_to_keras
import keras
import tensorflow as tf

def torch_to_onnx(net, input_shape, out_name="out/model.onnx", input_names=["input0"], output_names=["output0"], device="cpu"):
    batch_size = 1
    if len(input_shape) == 3:
        x = torch.randn(batch_size, input_shape[0], input_shape[1], input_shape[2], dtype=torch.float32).to(device)
    elif len(input_shape) == 1:
        x = torch.randn(batch_size, input_shape[0], dtype=torch.float32).to(device)
    else:
        raise Exception("not support input shape")
    print("input shape:", x.shape)
    # torch.onnx._export(net, x, "out/conv0.onnx", export_params=True)
    torch.onnx.export(net, x, out_name, export_params=True, input_names = input_names, output_names=output_names)
    print("export onnx ok")

def onnx_to_ncnn(input_shape, onnx="out/model.onnx", ncnn_param="out/conv0.param", ncnn_bin = "out/conv0.bin"):
    import os
    # onnx2ncnn tool compiled from ncnn/tools/onnx, and in the buld dir
    cmd = f"onnx2ncnn {onnx} {ncnn_param} {ncnn_bin}"       #更换自己的路径
    os.system(cmd)
    with open(ncnn_param) as f:
        content = f.read().split("\n")
        if len(input_shape) == 1:
            content[2] += " 0={}".format(input_shape[0])
        else:
            content[2] += " 0={} 1={} 2={}".format(input_shape[2], input_shape[1], input_shape[0])
        content = "\n".join(content)
    with open(ncnn_param, "w") as f:
        f.write(content)

def gen_input(input_shape, input_img=None, out_img_name="out/img.jpg", out_bin_name="out/input_data.bin", norm_int8=False):
    from PIL import Image
    if not input_img:
        input_img = (255, 0, 0)
    if type(input_img) == tuple:
        img = Image.new("RGB", (input_shape[2], input_shape[1]), input_img)
    else:
        img = Image.open(input_img)
        img = img.resize((input_shape[2], input_shape[1]))
    img.save(out_img_name)
    with open(out_bin_name, "wb") as f:
        print("norm_int8:", norm_int8)
        if not norm_int8:
            f.write(img.tobytes())
        else:
            data = (np.array(list(img.tobytes()), dtype=np.float)-128).astype(np.int8)
            f.write(bytes(data))

def onnx2pb(onnx_input_path="out/model.onnx", pb_output_path="out/model.pb"):
    onnx_model = onnx.load(onnx_input_path)  # load onnx model
    tf_exp = prepare(onnx_model)  # prepare tf representation
    tf_exp.export_graph(pb_output_path)  # export the model

def pb_to_tftile(onnx_input_path="out/model.pb", pb_output_path="out/model.tflite"):
    converter = tf.lite.TFLiteCOnverter.from_saved_model(onnx_input_path)
    converter.target_spec,supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINGS,tf.lite.OpsSet.SELECT_TF_OPS]
    tflite_model = converter.convert()
    with open(pb_output_path,'wb') as f:
        f.write(tflite_model)

def onnx2h5(onnx_input_path="out/model.onnx", pb_output_path="out/model.h5"):
    '''
    将.onnx模型保存为.h5文件模型,并打印出模型的大致结构
    '''
    onnx_model = onnx.load(onnx_input_path)
    k_model = onnx_to_keras(onnx_model, ["input0"])
    keras.models.save_model(k_model, pb_output_path, overwrite=True, include_optimizer=True)    #第二个参数是新的.h5模型的保存地址及文件名
    # # 下面内容是加载该模型，然后将该模型的结构打印出来
    # model = tf.keras.models.load_model('kerasModel.h5')
    # model.summary()
    # print(model)

def h5_to_tftile(onnx_input_path="out/model.h5", pb_output_path="out/model.tflite"):
    model = tf.keras.models.load_model(onnx_input_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    with open(pb_output_path,'wb') as f:
        f.write(tflite_model)

def ncnn_to_awnn(ncnn_param="out/conv0.param", ncnn_bin = "out/conv0.bin", imagePath="/out/images",outputPath="data/custom/"):
    import os
    print(os.getcwd())
    CURRENT_DIR = os.getcwd()
    cmd = CURRENT_DIR + "/v831_yolo/convert/spnntools optimize " + ncnn_param + " " + ncnn_bin + " " + outputPath + "/opt.param " + outputPath + "/opt.bin && " + CURRENT_DIR + "/v831_yolo/convert/spnntools calibrate -p=" + outputPath + "/opt.param -b=" + outputPath + "/opt.bin -i=" + imagePath + " -o=" + outputPath + "/opt.table -m=127.5,127.5,127.5 -n=0.0078125,0.0078125,0.0078125 -c=swapRB -t=3 &&  "+ CURRENT_DIR + "/v831_yolo/convert/spnntools quantize " + outputPath + "/opt.param " + outputPath + "/opt.bin " + outputPath + "/yolov2.param " + outputPath + "/yolov2.bin " + outputPath + "/opt.table" 
    os.system(cmd)