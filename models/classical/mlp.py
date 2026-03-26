import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
def Model(File_Jsonl,File_Title):
    def load_data(file_path):
        X, y = [], []
        with open(file_path, 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                X.append(data['func'])
                y.append(data['target'])
        return np.array(X), np.array(y)

    def split_data(X, y, test_size=0.2):
        return train_test_split(X, y, test_size=test_size, random_state=42)

    # 定义 MLP 模型
    class MLP(nn.Module):
        def __init__(self, input_size, hidden_size, num_classes):
            super(MLP, self).__init__()
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.fc2 = nn.Linear(hidden_size, num_classes)
            
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    # 修改训练函数，从图数据中取出特征来训练 MLP
    def train_model(model, features, labels, epochs=3300, lr=0.01):
        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        for epoch in range(epochs):
            logits = model(features)
            loss = criterion(logits, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}')

    # 修改评估函数，从图数据中取出特征来评估 MLP
    def evaluate_model(model, features, labels):
        model.eval()
        with torch.no_grad():
            logits = model(features)
            _, predicted = torch.max(logits, 1)
            acc = accuracy_score(labels.numpy(), predicted.numpy())
            f1 = f1_score(labels.numpy(), predicted.numpy())
            precision = precision_score(labels.numpy(), predicted.numpy())
            recall = recall_score(labels.numpy(), predicted.numpy())
        print('MLP:'+File_Title+':'+f'Accuracy: {acc:.4f}, F1 Score: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}')

    # 修改 main 函数
    X, y = load_data(File_Jsonl)
    X_train, X_test, y_train, y_test = split_data(X, y)

    features_train = torch.FloatTensor(X_train)
    features_test = torch.FloatTensor(X_test)
    
    labels_train = torch.LongTensor(y_train)
    labels_test = torch.LongTensor(y_test)

    input_size = X_train.shape[1]
    hidden_size = 64
    num_classes = len(np.unique(y_train))
        
    model = MLP(input_size, hidden_size, num_classes)
    train_model(model, features_train, labels_train)
    evaluate_model(model, features_test, labels_test)

Model('AST_Emberding_code.jsonl','AST')
Model('CFG_Emberding_code.jsonl','CFG')
Model('CPG_Emberding_code.jsonl','CPG')
Model('PDG_Emberding_code.jsonl','PDG')
