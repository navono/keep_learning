import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from urllib import request
import gzip

filename = [
    ["training_images", "train-images-idx3-ubyte.gz"],
    ["test_images", "t10k-images-idx3-ubyte.gz"],
    ["training_labels", "train-labels-idx1-ubyte.gz"],
    ["test_labels", "t10k-labels-idx1-ubyte.gz"]
]


def download_mnist():
    base_url = "http://yann.lecun.com/exdb/mnist/"
    for name in filename:
        print("Downloading " + name[1] + "...")
        request.urlretrieve(base_url + name[1], name[1])
    print("Download complete.")


def save_mnist():
    # mnist = {}
    # for name in filename[:2]:
    #     with gzip.open(name[1], 'rb') as f:
    #         mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)
    # for name in filename[-2:]:
    #     with gzip.open(name[1], 'rb') as f:
    #         mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    # with open("mnist.pkl", 'wb') as f:
    #     pickle.dump(mnist, f)
    # print("Save complete.")
    data_dict = {}
    for name in filename[:2]:
        with gzip.open(name[1], 'rb') as f:
            data_dict[name[0]] = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)
    for name in filename[-2:]:
        with gzip.open(name[1], 'rb') as f:
            data_dict[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)

        # Convert to pandas DataFrame
    train_images_df = pd.DataFrame(data_dict["training_images"])
    train_labels_df = pd.DataFrame(data_dict["training_labels"], columns=['label'])
    test_images_df = pd.DataFrame(data_dict["test_images"])
    test_labels_df = pd.DataFrame(data_dict["test_labels"], columns=['label'])

    # Save DataFrames as Parquet files
    train_images_df.to_parquet('training_images.parquet')
    train_labels_df.to_parquet('training_labels.parquet')
    test_images_df.to_parquet('test_images.parquet')
    test_labels_df.to_parquet('test_labels.parquet')

    print("Save complete.")


def init():
    download_mnist()
    save_mnist()


def load():
    # with open("mnist.pkl", 'rb') as f:
    #     mnist = pickle.load(f)
    # return mnist["training_images"], mnist["training_labels"], mnist["test_images"], mnist["test_labels"]

    train_images_df = pd.read_parquet('training_images.parquet')
    train_labels_df = pd.read_parquet('training_labels.parquet')
    test_images_df = pd.read_parquet('test_images.parquet')
    test_labels_df = pd.read_parquet('test_labels.parquet')

    return (train_images_df.values,
            train_labels_df['label'].values,
            test_images_df.values,
            test_labels_df['label'].values)
