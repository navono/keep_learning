import os
import torch
import torch.onnx as onnx
import numpy as np
import onnxruntime

from app.training.fnn import ForwardNeuralNet
from app.training.cnn import ConvNeuralNet
from app.training.rnn import RecurrentNeuralNet


def export_onnx(train_type, mode_path):
    # 检查模型文件是否存在
    if not os.path.exists(mode_path):
        return "模型文件: {} 不存在".format(mode_path)
    if train_type is None:
        return "请选择模型类型。"

    print("start export onnx with mode: ", mode_path)

    model = None
    dummy_input = None
    if train_type == "前馈神经网络（FNN）":
        model = ForwardNeuralNet()
        # 输入数据预处理
        # images: (batch_size, sequence_length*input_size)
        dummy_input = torch.randn(1, 1, 28, 28)
        input_shape = dummy_input.shape
        input_size = input_shape[1] * input_shape[2] * input_shape[3]
        dummy_input = dummy_input.view(-1, input_size)

    elif train_type == "卷积神经网络（CNN）":
        model = ConvNeuralNet()
        # 输入数据预处理
        # images: (batch_size, count, sequence_length, input_size)
        dummy_input = torch.randn(1, 1, 28, 28)
        dummy_input = dummy_input.view(-1, 1, 28, 28)

    elif train_type == "循环神经网络（RNN）":
        model = RecurrentNeuralNet()
        # 输入数据预处理
        # images: (batch_size, sequence_length, input_size)
        dummy_input = torch.randn(1, 28, 28)
        dummy_input = dummy_input.view(-1, 28, 28)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        dummy_input = dummy_input.to(device)

    if model is None or dummy_input is None:
        print("模型为空 或 导出 的 input 为空")
        return

    model.load_state_dict(torch.load(mode_path))
    # 将模型设置为评估模式
    model.eval()

    # 导出onnx模型
    onnx_path = mode_path.replace(".pt", ".onnx")
    onnx.export(model, dummy_input, onnx_path, verbose=True, input_names=['input'], output_names=['output'])

    return "导出 onnx 模型成功: {}".format(onnx_path)


def run_onnx(inference_type, image_data) -> tuple:
    if inference_type is None:
        return None, "请选择模型类型。"

    onnx_path = None

    if inference_type == "前馈神经网络（FNN）":
        onnx_path = './model/MNIST_FNN_model.onnx'
        image_data = image_data.reshape(-1, 28 * 28)
        # （1, 784）

    elif inference_type == "卷积神经网络（CNN）":
        onnx_path = './model/MNIST_CNN_model.onnx'
        image_data = image_data.unsqueeze(0)
        # （1, 1, 28, 28）

    elif inference_type == "循环神经网络（RNN）":
        onnx_path = './model/MNIST_RNN_model.onnx'
        # （1, 28, 28）

    if not os.path.exists(onnx_path):
        print("模型不存在，请先训练模型")
        return None, "模型不存在，请先训练模型"

    # 使用 ONNX Runtime 进行推理
    session = onnxruntime.InferenceSession(onnx_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    # 将输入数据类型转换为浮点数
    # image_data = image_data.astype(np.float32)
    image_data = image_data.numpy()
    print("image_data shape: ", image_data.shape)

    # 推理
    result = session.run([output_name], {input_name: image_data})

    # 打印推理结果
    print("ONNX Runtime Inference Result:", result)
    return result, None
