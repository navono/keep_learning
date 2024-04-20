# 转换

```
# 将 .pt 转换成 .onnx 格式
python export-det.py --weights yolov8s.pt --iou-thres 0.65 --conf-thres 0.25 --topk 100 --opset 11 --sim --input-shape 1 3 640 640 --device cuda:0

# 将 .onnx 转换成 .engine(trt)
trtexec --onnx=E:\\sourcecode\\cpp\\YOLOv8-TensorRT\\yolov8s.onnx --saveEngine=E:\\sourcecode\\cpp\\YOLOv8-TensorRT\\yolov8s.engine --fp16

```