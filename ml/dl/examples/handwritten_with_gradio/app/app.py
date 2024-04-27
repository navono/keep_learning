import gradio as gr
from PIL import Image
from torchvision import transforms
import numpy as np

from app.training import train_fnn, train_cnn, train_rnn
from app.inference import export_onnx, run_onnx

global_train_type = ""
global_inference_type = None


def inference(infer_model_typen, img_data):
    if infer_model_typen == "":
        return "请选择推理模型。"
    if img_data is None:
        return "请绘制数字。"

    # 将 Gradio Sketchpad 绘制的图片数据转换为 PIL 图像对象
    pil_image = Image.fromarray(img_data)

    # 调整图片大小为目标尺寸
    resized_image = pil_image.resize((28, 28), Image.ANTIALIAS)

    # 将调整后的图片转换为 NumPy 数组
    raw_data = resized_image.getdata()
    img_array = np.asarray(raw_data, dtype=np.uint8).reshape(resized_image.size[1], resized_image.size[0])
    img_tensor = transforms.ToTensor()(img_array)

    result, err = run_onnx(infer_model_typen, img_tensor)
    if err is not None:
        return err

    # 选出概率最大的一个
    pred = np.argmax(result)
    return pred.item()


def train():
    if global_train_type is None:
        return "请选择模型类型。"
    elif global_train_type == "前馈神经网络（FNN）":
        done_msg, model_path = train_fnn()
        export_onnx(global_train_type, model_path)
        return done_msg
    elif global_train_type == "卷积神经网络（CNN）":
        done_msg, model_path = train_cnn()
        export_onnx(global_train_type, model_path)
        return done_msg
    elif global_train_type == "循环神经网络（RNN）":
        done_msg, model_path = train_rnn()
        export_onnx(global_train_type, model_path)
        return done_msg
    else:
        return "请选择模型类型。"


def change_train_type(choose_train_type):
    global global_train_type
    global_train_type = choose_train_type
    return "已选择：" + global_train_type + " 模型。"


def launch():
    with gr.Blocks() as hand_written:
        gr.Markdown("# Handwritten Digit Recognizer")

        with gr.Column():
            gr.Markdown("## 预测")
            sketch_input = gr.Sketchpad(shape=(300, 300))

        with gr.Row():
            global global_inference_type
            infer_model_type = gr.Dropdown(["前馈神经网络（FNN）", "卷积神经网络（CNN）", "循环神经网络（RNN）"],
                                           label="选择推理模型")
            infer_result_output = gr.Text(placeholder="预测结果")

        with gr.Row():
            clear_img_btn = gr.Button("清除")
            inference_img_btn = gr.Button("预测")

        inference_img_btn.click(inference, inputs=[infer_model_type, sketch_input], outputs=infer_result_output)

        with gr.Column():
            gr.Markdown("## 训练")
            radio = gr.Radio(
                ["前馈神经网络（FNN）", "卷积神经网络（CNN）", "循环神经网络（RNN）"], label="可选模型类型")
            text = gr.Textbox(lines=2, interactive=False, label="已选模型")
            train_process = gr.Textbox(lines=2, interactive=False, label="训练过程")
            radio.change(fn=change_train_type, inputs=radio, outputs=text)

            with gr.Column():
                train_button = gr.Button("训练")

        train_button.click(train, outputs=train_process)

    hand_written.launch(share=True, debug=True)
