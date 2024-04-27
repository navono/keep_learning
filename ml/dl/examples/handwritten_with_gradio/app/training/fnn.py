import os
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters
input_size = 784  # 28*28
hidden_size = 512
num_classes = 10
num_epochs = 5
batch_size = 100
learning_rate = 0.001

# MNIST dataset
train_dataset = torchvision.datasets.MNIST(root='./data',
                                           train=True,
                                           transform=transforms.ToTensor(),
                                           download=True)

test_dataset = torchvision.datasets.MNIST(root='./data',
                                          train=False,
                                          transform=transforms.ToTensor())

# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size,
                                          shuffle=False)


# Fully connected neural network with one hidden layer
# 处理的数据维度是（1,28*28）
class ForwardNeuralNet(nn.Module):
    """
        另一个就是使用 nonlinear model
        linear1 = torch.nn.Linear(input_size, hidden_size, bias = True)
        linear2 = torch.nn.Linear(hidden_size, num_classes, bias = True)
        relu = torch.nn.ReLU()

        model = torch.nn.Sequential(linear1, relu, linear2)
    """

    def __init__(self, input_size=input_size, hidden_size=hidden_size, num_classes=num_classes):
        super(ForwardNeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


def train_fnn() -> tuple:
    model_path = './model/MNIST_FNN_model.pt'
    if os.path.exists(model_path):
        return "模型文件: {} 已存在".format(model_path), model_path

    print("start training fnn with mode: ", device)
    model = ForwardNeuralNet(input_size, hidden_size, num_classes).to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            images = images.reshape(-1, 28 * 28).to(device)
            # print("images shape: ", images.shape)
            # images: (batch_size, sequence_length*input_size)

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
