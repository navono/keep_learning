import datetime
import math
import time
import cv2
import multiprocessing
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from pathlib import Path
import more_itertools
import torch

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

OCR_SLICE = {'horizontal_stride': 960, 'vertical_stride': 960,
             'merge_x_thres': 15, 'merge_y_thres': 15}


def worker(gpu_id, image_paths, result_list, lock):
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(lang="ch", show_log=False,
                    use_gpu=True,
                    gpu_id=gpu_id,
                    det_model_dir="./model_weight/ocr/ch_PP-OCRv4_det_server_infer",
                    rec_model_dir="./model_weight/ocr/ch_PP-OCRv4_rec_server_infer")

    for image_path in image_paths:
        current_datetime = datetime.datetime.now()
        print(
            f'GPU [{gpu_id}] {current_datetime.strftime("%Y-%m-%d %H:%M:%S")} image_path: ', image_path)

        image = cv2.imdecode(np.fromfile(Path(image_path), dtype=np.uint8), -1)
        img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = ocr.ocr(img, cls=False, slice=OCR_SLICE)

        lock.acquire()
        result_list.append([image_path, results])
        lock.release()


def single_gpu_process(process_per_gpu):
    lock = multiprocessing.Lock()
    start_time = time.time()

    img_root_dir = os.getcwd() + "/example_data/2"
    img_files = [img_root_dir + "/" +
                 f for f in os.listdir(img_root_dir) if f.endswith('.png')]

    manager = multiprocessing.Manager()
    results = manager.list()
    processes = []
    per_process = math.ceil(len(img_files) / process_per_gpu)

    for i in range(0, process_per_gpu):
        cur_image_paths = img_files[i *
                                    per_process:(i + 1) * per_process]
        if i == process_per_gpu - 1:
            cur_image_paths = img_files[i * per_process:]

        print('cur_image_paths: ', len(cur_image_paths))

        p = multiprocessing.Process(target=worker, args=(
            0, cur_image_paths, results, lock))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("process results: ", len(results))
    end_time = time.time()
    print("ocr time: {}".format(end_time - start_time))
    # draw_ocr(result_list)


def multi_gpu_process():
    img_root_dir = os.getcwd() + "/example_data/2"
    img_files = [img_root_dir + "/" +
                 f for f in os.listdir(img_root_dir) if f.endswith('.png')]

    # gpu_count = torch.cuda.device_count()
    gpu_count = 2
    batched_data = list(more_itertools.chunked(
        img_files, len(img_files) // gpu_count + 1))

    queue = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    results = manager.list()
    lock = multiprocessing.Lock()

    start_time = time.time()
    processes = []

    # 4: 86
    # 5: 74
    # 6: 70
    # 7: 68
    # 8: 60
    process_per_gpu = 8

    for gpu_id in range(gpu_count):
        gpu_data_list = batched_data[gpu_id]
        print(f"GPU {gpu_id}: images count: {len(gpu_data_list)}")

        # per_process = len(gpu_data_list) // process_per_gpu
        per_process = math.ceil(len(gpu_data_list) / process_per_gpu)

        for i in range(0, process_per_gpu):
            cur_image_paths = gpu_data_list[i *
                                            per_process:(i + 1) * per_process]
            if i == process_per_gpu - 1:
                cur_image_paths = gpu_data_list[i * per_process:]

            print('cur_image_paths: ', len(cur_image_paths))

            p = multiprocessing.Process(target=worker, args=(
                gpu_id, cur_image_paths, results, lock))
            p.start()
            processes.append(p)

    for p in processes:
        p.join()

    print("process results: ", len(results))
    end_time = time.time()
    print("ocr time: {}".format(end_time - start_time))
    # draw_ocr(results)


def get_gpu_memory():
    torch.cuda.empty_cache()  # 清空缓存，确保显存信息最新
    gpu_memory = []
    for i in range(torch.cuda.device_count()):
        gpu = torch.cuda.get_device_properties(i)
        memory = gpu.total_memory / 1024 ** 3  # 显存总量，单位为 GB
        print(f"GPU {i}: {memory:.2f} GB")
        gpu_memory.append(memory)
    return gpu_memory


if __name__ == '__main__':
    import torch

    torch.multiprocessing.set_start_method("spawn")

    # import paddle
    # paddle.utils.run_check()

    gpus_memory = get_gpu_memory()
    mem_per_process = 3
    process_per_gpu = int(gpus_memory[0] // mem_per_process)
    # 4: 91
    single_gpu_process(4)

    # multi_gpu_process()
