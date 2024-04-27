import os

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

# Device configuration
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Hyper parameters
num_epochs = 5
num_classes = 10
batch_size = 100
learning_rate = 0.001

# MNIST dataset
train_dataset = torchvision.datasets.MNIST(root='./data/',
                                           train=True,
                                           transform=transforms.ToTensor(),
                                           download=True)

test_dataset = torchvision.datasets.MNIST(root='./data/',
                                          train=False,
                                          transform=transforms.ToTensor())

# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size,
                                          shuffle=False)


# Convolutional neural network (two convolutional layers)
# 处理的数据维度是（1,1,28,28）
class ConvNeuralNet(nn.Module):
    def __init__(self, num_classes=10):
        super(ConvNeuralNet, self).__init__()
        self.layer1 = nn.Sequential(
            # [1, 28, 28] -> [16, 28, 28]
            nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            # [16, 28, 28]
            nn.BatchNorm2d(16),
            # [16, 28, 28]
            nn.ReLU(),
            # [16, 28, 28] -> [16, 14, 14]
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            # [16, 14, 14] -> [32, 14, 14]
            nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            # [32, 14, 14]
            nn.BatchNorm2d(32),
            # [32, 14, 14]
            nn.ReLU(),
            # [32, 14, 14] -> [32, 7, 7]
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(7 * 7 * 32, num_classes)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out


def train_cnn() -> tuple:
    model_path = "./model/MNIST_CNN_model.pt"
    if os.path.exists(model_path):
        return "模型文件: {} 已存在".format(model_path), model_path

    print("start training cnn with mode: ", device)
    model = ConvNeuralNet(num_classes).to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # 根据模型的输入不同，需要将数据转换为不同的形式
            images = images.to(device)
            # print("images shape: ", images.shape)
            # images: (batch_size, count, sequence_length, input_size)

            labels = labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

    torch.save(model.state_dict(), model_path)
    done_msg = "训练完成。"
    print(done_msg)
    return done_msg, model_path
