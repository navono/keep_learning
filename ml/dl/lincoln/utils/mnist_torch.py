# import torchvision
# import torchvision.transforms as transforms
#
# # 定义数据转换
# transform = transforms.Compose([transforms.ToTensor()])
#
# # 下载并加载训练集
# trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
# trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
#
# # 下载并加载测试集
# testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
# testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False)
#
# # 打印数据集大小
# print(f"Number of training samples: {len(trainset)}")
# print(f"Number of testing samples: {len(testset)}")
#
#

from torchvision import datasets


def init():
    train_data = datasets.MNIST(root="./data/", train=True, download=True)
    test_data = datasets.MNIST(root="./data/", train=False, download=True)
    return train_data, test_data
