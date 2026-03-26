import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import lightgbm as lgb #lightgbm is an implementation of GBDT

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

def train_model(X_train, y_train, num_round=3300):
    lgb_train = lgb.Dataset(X_train, y_train)
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'verbose': -1
    }
    model = lgb.train(params, lgb_train, num_boost_round=num_round)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test, num_iteration=model.best_iteration)
    y_pred_binary = np.round(y_pred)
    acc = accuracy_score(y_test, y_pred_binary)
    f1 = f1_score(y_test, y_pred_binary)
    precision = precision_score(y_test, y_pred_binary)
    recall = recall_score(y_test, y_pred_binary)
    return acc, f1, precision, recall

def Model(Graph_Jsonl,Graph_Name):
    X, y = load_data(Graph_Jsonl)# 加载数据
    X_train, X_test, y_train, y_test = split_data(X, y)# 划分数据集
    
    model = train_model(X_train, y_train)# 训练模型
    acc, f1, precision, recall = evaluate_model(model, X_test, y_test)# 评估模型
    
    print('GBDT:'+Graph_Name+f': Accuracy: {acc:.4f}, F1 Score: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}')



Model('AST_Emberding_code.jsonl','AST')
Model('CFG_Emberding_code.jsonl','CFG')
Model('CPG_Emberding_code.jsonl','CPG')
Model('PDG_Emberding_code.jsonl','PDG')
