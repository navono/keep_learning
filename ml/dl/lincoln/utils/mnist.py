import numpy as np
from urllib import request
import gzip
import pickle

# MNIST 数据集文件名及其替代 URL
filename = [
    ["training_images", "train-images-idx3-ubyte.gz"],
    ["test_images", "t10k-images-idx3-ubyte.gz"],
    ["training_labels", "train-labels-idx1-ubyte.gz"],
    ["test_labels", "t10k-labels-idx1-ubyte.gz"]
]

# 使用替代的镜像源
base_url = "https://ossci-datasets.s3.amazonaws.com/mnist/"


def download_mnist():
    for name in filename:
        print("Downloading " + name[1] + "...")
        request.urlretrieve(base_url + name[1], name[1])
    print("Download complete.")


def save_mnist():
    mnist = {}
    for name in filename[:2]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)
    for name in filename[-2:]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    with open("mnist.pkl", 'wb') as f:
        pickle.dump(mnist, f)
    print("Save complete.")


def init():
    download_mnist()
    save_mnist()


def load():
    with open("mnist.pkl", 'rb') as f:
        mnist = pickle.load(f)
    return mnist["training_images"], mnist["training_labels"], mnist["test_images"], mnist["test_labels"]

# # 初始化下载和保存数据集
# init()
#
# # 加载数据集
# train_images, train_labels, test_images, test_labels = load()
# print(f"Training images shape: {train_images.shape}")
# print(f"Training labels shape: {train_labels.shape}")
# print(f"Test images shape: {test_images.shape}")
# print(f"Test labels shape: {test_labels.shape}")
