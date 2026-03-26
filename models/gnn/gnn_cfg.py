import json
import numpy as np
import dgl
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt

def load_data(file_path):
    X, y = [], []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            X.append(data['func'])
            y.append(data['target'])
    return np.array(X), np.array(y)

def split_data(X, y, test_size=0.2):
    return train_test_split(X, y, test_size=test_size, random_state=1000)

def create_graph(X_train, y_train):
    num_nodes = X_train.shape[0]
    g = dgl.graph((np.arange(num_nodes), np.arange(num_nodes)))  # Create an empty graph
    labels = torch.from_numpy(y_train)
    g.ndata['labels'] = labels
    features = torch.FloatTensor(X_train)
    g.ndata['features'] = features
    return g

# GNN model
class GNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(GNN, self).__init__()
        self.conv1 = dgl.nn.GraphConv(input_size, hidden_size)
        self.conv2 = dgl.nn.GraphConv(hidden_size, num_classes)

    def forward(self, g):
        x = g.ndata['features']
        x = self.conv1(g, x)
        x = torch.relu(x)
        x = self.conv2(g, x)
        return x

def train_model(model, g, labels, epochs=3300, lr=0.00155):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    losses = []  # 用于存储每一个epoch的损失

    for epoch in range(epochs):
        logits = model(g)
        loss = criterion(logits, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())  # 添加当前epoch的损失
        # print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}')

    return losses  # 返回每一个epoch的损失

# Evaluate
def evaluate_model(model, g, labels,title):
    model.eval()
    with torch.no_grad():
        logits = model(g)
        _, predicted = torch.max(logits, 1)
        acc = accuracy_score(labels, predicted.numpy())
        f1 = f1_score(labels, predicted.numpy())
        precision = precision_score(labels, predicted.numpy())
        recall = recall_score(labels, predicted.numpy())
    print('GNN-'+title+":"+f'Accuracy: {acc:.4f}, F1 Score: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}')

def Demo(Emberding_Jsonl,title):
    X, y = load_data(Emberding_Jsonl)
    X_train, X_test, y_train, y_test = split_data(X, y)

    g_train = create_graph(X_train, y_train)
   
    labels_train = torch.LongTensor(y_train)
    labels_test = torch.LongTensor(y_test)

    input_size = X_train.shape[1]
    hidden_size = 64
    num_classes = len(np.unique(y_train))
    model = GNN(input_size, hidden_size, num_classes)
    losses = train_model(model, g_train, labels_train)

    g_test = create_graph(X_test, y_test)
    evaluate_model(model, g_test, labels_test,title)

    # 绘制损失曲线
    plt.plot(losses)
    plt.xlabel('CFG')
    plt.ylabel('Loss')
    plt.title(title+':Training Loss')
    plt.grid(True)
    plt.show()

    

if __name__ == '__main__':
    Demo('CFG_Emberding_code.jsonl','CFG')
    # Demo('PDG_Emberding_code.jsonl','PDG')
    # Demo('AST_Emberding_code.jsonl','AST')







